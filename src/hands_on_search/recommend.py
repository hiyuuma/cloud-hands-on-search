"""T4: 推薦。空き時間・関心キーワード・計画月から候補を決定論的に選ぶ。

スコアリング (全て決定的、ランダム要素なし):
    score = 3 * タイトル/サービスへのキーワード一致数
          + 2 * 要約へのキーワード一致数
          + 2   計画月が一致する場合
          + 1   priority が高/中 (高=2, 中=1)
          - ペナルティなし
    同点は duration_min が短い方 → id の順 (完全に決定的)

候補選定は「合計所要時間が空き時間を超えない範囲でスコア合計を最大化」する
ナップサック DP (I3):
    duration_min 判明レコードについて 0/1 ナップサックを解き、空き時間内で
    スコア合計が最大の組合せを選ぶ。件数は limit まで。
    同スコアのタイは (合計時間が小さい方 → より前の候補) で決定的に解く。
    duration 不明のものは時間にカウントせず末尾に回す (上限を破らないため)。
    空き時間が大きすぎる場合 (全判明レコードの合計を超える) は DP を
    省略し、スコア順に limit 件を取る (このとき全件が常に収まるため最適)。

出力は候補リストと同伴型フォーマット「今日の流れと所要時間・課金の見立て」。
"""

_UNKNOWN_ACCESS = "不明・要確認"


def _haystack_title(r):
    return (
        (r.get("title") or "")
        + " "
        + (r.get("title_ja") or "")
        + " "
        + " ".join(r.get("services") or [])
    ).lower()


def _score(r, interests, plan_month):
    """(score, reasons) を返す。reasons は内訳 (なぜ選ばれたか)。"""
    score = 0
    reasons = []
    title_hay = _haystack_title(r)
    summary = (r.get("summary_ja") or "").lower()

    title_hits, summary_hits = [], []
    for kw in interests:
        kw_l = kw.lower()
        if kw_l in title_hay:
            title_hits.append(kw)
        elif kw_l in summary:
            summary_hits.append(kw)
    if interests and not (title_hits or summary_hits):
        return None, []

    if title_hits:
        score += 3 * len(title_hits)
        reasons.append("関心「" + "・".join(title_hits) + "」がタイトル/サービスに一致")
    if summary_hits:
        score += 2 * len(summary_hits)
        reasons.append("関心「" + "・".join(summary_hits) + "」が要約に一致")

    if plan_month and (r.get("plan_month") or "").startswith(plan_month):
        score += 2
        reasons.append(f"計画月 {plan_month} のタスク")

    if r.get("priority") == "高":
        score += 2
        reasons.append("優先度「高」")
    elif r.get("priority") == "中":
        score += 1
        reasons.append("優先度「中」")

    if not reasons:
        reasons.append("絞り込み条件に合致")
    return score, reasons


def _access_note(r):
    a = (r.get("access") or "").strip()
    if not a or a.lower() == "unknown":
        return _UNKNOWN_ACCESS
    return a


def _pack_knapsack(known, minutes, limit):
    """duration_min 判明レコードの 0/1 ナップサックを DP で解く。

    known は決定的ソート済みの (score, rec, reasons) リスト (duration>0)。
    dp[w] = (最大スコア, 選んだ添字のタプル) とし、更新は厳密に
    スコア向上時のみ行うため同入力は常に同じ結果になる。
    タイの解は「より小さい合計時間 w」を優先する。
    """
    total = sum(r["duration_min"] for _, r, _ in known)
    if total <= minutes:
        # 全件収まる場合はスコア順に limit 件取るのが最適
        return known[:limit]
    if minutes > 20000:
        # 巨大な空き時間では DP 状態数が増えすぎるため、安全側として
        # 収まるものをスコア順に取る (実用上のフォールバック)
        picked = []
        used = 0
        for s, r, reasons in known:
            d = r["duration_min"]
            if used + d <= minutes and len(picked) < limit:
                picked.append((s, r, reasons))
                used += d
        return picked

    dp = {0: (0, ())}  # 合計時間 -> (スコア, 添字タプル)
    for i, (s, r, _) in enumerate(known):
        d = r["duration_min"]
        if d > minutes:
            continue
        additions = {}
        for w, (sc, idxs) in dp.items():
            nw = w + d
            if nw > minutes or len(idxs) >= limit:
                continue
            nsc = sc + s
            cur = dp.get(nw, additions.get(nw))
            if cur is None or nsc > cur[0]:
                additions[nw] = (nsc, idxs + (i,))
        dp.update(additions)

    best_score = max(sc for sc, _ in dp.values())
    # 同スコアでは合計時間が小さい方を選ぶ (決定的)
    best_w = min(w for w, (sc, _) in dp.items() if sc == best_score)
    return [known[i] for i in dp[best_w][1]]


def recommend(records, *, minutes, interests=(), plan_month=None, limit=10):
    """候補リストを返す。

    各候補は統一レコードに _score/_reasons を付けた dict。
    duration_min 不明のレコードは時間枠にカウントしない (上限を保証するため
    判明しているものだけを合計に含める)。
    """
    interests = [k for k in interests if k and k.strip()]

    scored = []
    for r in records:
        s, reasons = _score(r, interests, plan_month)
        if s is None:
            continue  # 関心指定がある場合、無関係なものは出さない
        scored.append((s, r, reasons))

    # 決定的ソート: スコア降順 → 所要時間昇順 (None は最後) → id
    scored.sort(
        key=lambda t: (-t[0], t[1].get("duration_min") is None,
                       t[1].get("duration_min") or 0, t[1]["id"])
    )

    known = [t for t in scored if t[1].get("duration_min") is not None]
    unknown = [t for t in scored if t[1].get("duration_min") is None]

    packed = _pack_knapsack(known, minutes, limit)
    # 出力順は従来どおりスコア順 (ソート順のまま)
    order = {id(r): i for i, (_, r, _) in enumerate(scored)}
    picked = [
        {**r, "_score": s, "_reasons": reasons}
        for s, r, reasons in sorted(packed, key=lambda t: order[id(t[1])])
    ]

    # duration 不明 (時間枠を消費しない) を空き枠の末尾に追加
    for s, r, reasons in unknown:
        if len(picked) >= limit:
            break
        picked.append({**r, "_score": s, "_reasons": reasons})

    return picked


def format_plan(picked, *, minutes, interests=(), plan_month=None):
    """同伴型フォーマット「今日の流れと所要時間・課金の見立て」を返す。"""
    total = sum(r["duration_min"] for r in picked if r.get("duration_min"))
    unknown_dur = sum(1 for r in picked if r.get("duration_min") is None)

    lines = []
    cond = []
    if plan_month:
        cond.append(f"計画月 {plan_month}")
    if interests:
        cond.append("関心: " + "・".join(interests))
    header = f"## 今日の流れ ({minutes}分の空き時間)"
    if cond:
        header += " — " + "、".join(cond)
    lines.append(header)
    lines.append("")

    if not picked:
        lines.append("条件に合う候補が見つかりませんでした。")
        return "\n".join(lines) + "\n"

    t = 0
    for i, r in enumerate(picked, 1):
        d = r.get("duration_min")
        if d is not None:
            span = f"{t}〜{t + d}分"
            t += d
            dur = f"{d}分"
        else:
            span = "時間外 (所要時間不明)"
            dur = "不明"
        link = r["link"]
        url = link.get("url") or "(URL なし)"
        kind = link.get("kind")
        lines.append(f"{i}. [{r['title']}]({url})")
        lines.append(
            f"   {span} / 所要時間 {dur} / {r.get('cloud') or '-'}"
            f" / link={kind}"
        )
        lines.append("   理由: " + "；".join(r["_reasons"]))
        lines.append("")

    lines.append(f"合計所要時間: {total}分 (空き {minutes}分以内)")
    if unknown_dur:
        lines.append(
            f"※ {unknown_dur}件は所要時間不明のため合計に含めていません"
            " (実際には超える可能性があります)"
        )
    lines.append("")
    lines.append("## 課金の見立て")
    for r in picked:
        lines.append(f"- {r['title']}: {_access_note(r)}")
    lines.append("")
    lines.append(
        "※ 上記はカタログの access 表記 (Subscription / Free / credits 等)"
        " に基づく区分であり、金額の推測はしません。"
        " 不明なものは「不明・要確認」としています。"
    )
    return "\n".join(lines) + "\n"
