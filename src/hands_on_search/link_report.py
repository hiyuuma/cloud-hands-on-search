"""カタログ別の link kind (direct/search/none) 集計レポート"""

from collections import Counter


def link_report(records):
    """{catalog: {direct, search, none, total}} を返す。"""
    report = {}
    for rec in records:
        cat = rec["source_catalog"]
        kind = (rec.get("link") or {}).get("kind") or "none"
        c = report.setdefault(cat, Counter())
        c[kind] += 1
        c["total"] += 1
    return {
        cat: {
            "total": c["total"],
            "direct": c.get("direct", 0),
            "search": c.get("search", 0),
            "none": c.get("none", 0),
        }
        for cat, c in sorted(report.items())
    }


def link_report_markdown(records):
    report = link_report(records)
    lines = [
        "| catalog | total | direct | search | none |",
        "|---|---|---|---|---|",
    ]
    for cat, c in report.items():
        lines.append(
            f"| {cat} | {c.get('total', 0)} | {c.get('direct', 0)} "
            f"| {c.get('search', 0)} | {c.get('none', 0)} |"
        )
    return "\n".join(lines) + "\n"
