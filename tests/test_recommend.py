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
    # 貪欲パックなので各採用時点で残り時間内に収まっている
    assert sum(known) <= 45


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
