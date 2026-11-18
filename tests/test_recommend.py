"""T4: 推薦のテスト"""

from hands_on_search.recommend import format_plan, recommend


def test_deterministic(records):
    a = recommend(records, minutes=90, interests=["MCP", "コンテナ"])
    b = recommend(records, minutes=90, interests=["MCP", "コンテナ"])
    assert [r["id"] for r in a] == [r["id"] for r in b]


def test_respects_time_budget(records):
    picked = recommend(records, minutes=60, interests=["コンテナ"])
    total = sum(r["duration_min"] for r in picked if r.get("duration_min"))
    assert total <= 60


def test_every_item_fits_or_unknown_duration(records):
    picked = recommend(records, minutes=45, interests=["Kubernetes"])
    known = [r["duration_min"] for r in picked if r.get("duration_min")]
    # ナップサック DP なので判明している所要時間の合計は必ず枠内
    assert sum(known) <= 45


def _mk(i, dur, score_hint):
    """テスト用の最小レコード。score_hint でタイトルに含める語数を変えて
    スコアを差別化する (interests は全てタイトルに含める)。"""
    return {
        "id": f"t:{i}",
        "source_catalog": "plan",
        "title": " ".join(score_hint) + f" lab{i}",
        "title_ja": None,
        "summary_ja": None,
        "cloud": "AWS",
        "services": [],
        "domain": None,
        "level": None,
        "levels": [],
        "duration_min": dur,
        "access": None,
        "priority": None,
        "plan_month": None,
        "plan_theme": None,
        "link": {"url": "", "kind": "none", "source": "plan"},
        "related": [],
        "raw": {},
    }


def test_knapsack_beats_greedy():
    """I3: 貪欲 (スコア順) では最適にならない入力で DP がより高い
    スコア合計を選ぶ。

    A: 60分 score=6 (語2つ一致), B/C: 30分 score=3 (語1つ一致)。
    空き60分。貪欲は A(60分,6) のみ → 合計6。DP は B+C(60分,6)…
    ではなく、A に語を3つ持たせて貪欲の罠を作る。
    A: 60分 score=9 / B,C: 30分 score=6ずつ → 貪欲 A=9, DP B+C=12。
    """
    a = _mk("a", 60, ["alpha", "beta", "gamma"])
    b = _mk("b", 30, ["alpha", "beta"])
    c = _mk("c", 30, ["alpha", "beta"])
    interests = ["alpha", "beta", "gamma"]
    picked = recommend([a, b, c], minutes=60, interests=interests)
    ids = {r["id"] for r in picked}
    assert ids == {"t:b", "t:c"}
    assert sum(r["_score"] for r in picked) == 12


def test_knapsack_deterministic():
    recs = [
        _mk("a", 60, ["alpha", "beta", "gamma"]),
        _mk("b", 30, ["alpha", "beta"]),
        _mk("c", 30, ["alpha", "beta"]),
        _mk("d", 15, ["alpha"]),
    ]
    interests = ["alpha", "beta", "gamma"]
    x = recommend(recs, minutes=60, interests=interests)
    y = recommend(recs, minutes=60, interests=interests)
    assert [r["id"] for r in x] == [r["id"] for r in y]
    assert sum(r["duration_min"] for r in x) <= 60


def test_knapsack_respects_limit():
    # 件数上限 limit も DP の制約として効く
    recs = [_mk(str(i), 10, ["alpha"]) for i in range(5)]
    picked = recommend(recs, minutes=60, interests=["alpha"], limit=2)
    assert len(picked) <= 2


def test_reasons_attached(records):
    picked = recommend(records, minutes=90, interests=["MCP"])
    assert picked
    for r in picked:
        assert r["_reasons"], r["id"]
        assert r["_score"] > 0


def test_interest_matching(records):
    picked = recommend(records, minutes=200, interests=["Fargate"])
    assert any(
        "Fargate" in (r["title"] or "") or
        any("Fargate" in s for s in r["services"])
        for r in picked
    )


def test_plan_month_boost(records):
    # plan:HO-SAMPLE-003 (Fargate, plan_month=2026-11) がブーストされる
    month = "2026-11"
    picked = recommend(records, minutes=300, interests=["Fargate"],
                       plan_month=month, limit=50)
    plan_hits = [
        r for r in picked
        if (r["plan_month"] or "").startswith(month)
    ]
    assert plan_hits, "計画月一致レコードが候補に無い"
    assert any("計画月" in reason for r in plan_hits for reason in r["_reasons"])


def test_format_plan_text(records):
    picked = recommend(records, minutes=90, interests=["MCP", "コンテナ"])
    text = format_plan(picked, minutes=90,
                       interests=["MCP", "コンテナ"], plan_month=None)
    assert "今日の流れ" in text
    assert "合計所要時間" in text
    assert "課金の見立て" in text
    # 全タイトルが Markdown リンク (URL 導線)
    for r in picked:
        assert f"[{r['title']}](" in text
    # access 不明は正直に
    assert "金額の推測はしません" in text


def test_unknown_access_marked(records):
    # access が空/unknown のレコードは「不明・要確認」になる
    rec = next(
        r for r in records
        if not (r.get("access") or "").strip()
        or r["access"].lower() == "unknown"
    )
    from hands_on_search.recommend import _access_note
    assert _access_note(rec) == "不明・要確認"


def test_empty_result(records):
    picked = recommend(records, minutes=1, interests=["存在しない語xyz"])
    assert picked == []
    text = format_plan(picked, minutes=1, interests=["存在しない語xyz"])
    assert "見つかりませんでした" in text
