"""T2: カタログ横断リンク。

正規化タイトル一致・URL一致で異なるカタログの同一ラボ候補を related に記録する。
削除・マージはしない。related 先に direct URL があり自レコードに無い場合は
link を direct に格上げし、source に引き継ぎ元カタログを記録する。
"""

from .normalize import normalize_title, normalize_url


def _group_key_candidates(rec):
    keys = set()
    for t in (rec.get("title"), rec.get("title_ja")):
        k = normalize_title(t)
        if k:
            keys.add(("title", k))
    url = rec.get("link", {}).get("url") or ""
    if rec.get("link", {}).get("kind") == "direct" and url:
        keys.add(("url", normalize_url(url)))
    return keys


def build_related(records):
    """records の related を相互参照 ID リストとして埋め、link 格上げを行う。"""
    groups = {}
    for rec in records:
        for key in _group_key_candidates(rec):
            groups.setdefault(key, []).append(rec)

    changed = 0
    for key, group in groups.items():
        catalogs = {r["source_catalog"] for r in group}
        if len(catalogs) < 2:
            continue
        ids = [r["id"] for r in group]
        for rec in group:
            others = sorted(i for i in ids if i != rec["id"])
            rec["related"] = sorted(set(rec.get("related") or []) | set(others))

    # link 格上げ: related 先の direct URL を引き継ぐ
    by_id = {r["id"]: r for r in records}
    for rec in records:
        link = rec.get("link") or {}
        if link.get("kind") == "direct":
            continue
        donor = next(
            (
                by_id[rid]
                for rid in rec.get("related") or []
                if (by_id[rid].get("link") or {}).get("kind") == "direct"
                and by_id[rid]["link"].get("url")
            ),
            None,
        )
        if donor:
            rec["link"] = {
                "url": donor["link"]["url"],
                "kind": "direct",
                "source": donor["source_catalog"],
            }
            changed += 1
    return changed
