"""T5: コマンドラインインターフェース。

    python3 -m hands_on_search.cli search <query> [--cloud AWS] [--max-minutes 60] [--limit 10]
    python3 -m hands_on_search.cli recommend [--minutes 90] [--interest MCP コンテナ] [--month 2026-11]
    python3 -m hands_on_search.cli show <id>
    python3 -m hands_on_search.cli stats
    python3 -m hands_on_search.cli export-plan [--minutes 90] [--interest ...] [--out plan.md]

build/catalog.db が無ければ自動で ETL を実行して生成する。
"""

import argparse
import sqlite3
import sys
from collections import Counter
from pathlib import Path

from .db import _COLUMNS, row_to_record
from .etl import BUILD_DIR, run_etl
from .recommend import format_plan, recommend
from .search import search

DB_PATH = BUILD_DIR / "catalog.db"


def _ensure_db(path=None):
    path = Path(path or DB_PATH)
    if not path.exists():
        print(f"catalog.db が無いため ETL を実行します -> {path}", file=sys.stderr)
        run_etl()
    return path


def _link_str(rec):
    link = rec["link"]
    url = link.get("url") or "(URL なし)"
    return f"{url} [{link.get('kind')}]"


def cmd_search(args):
    db = _ensure_db()
    results = search(
        db,
        args.query,
        cloud=args.cloud,
        domain=args.domain,
        service=args.service,
        level=args.level,
        max_duration_min=args.max_minutes,
        access=args.access,
        priority=args.priority,
        plan_month=args.month,
        limit=args.limit,
    )
    print(f"{len(results)} 件ヒット")
    for i, r in enumerate(results, 1):
        d = r.get("duration_min")
        print(f"{i}. {r['title']}  ({r['id']})")
        print(
            f"   {r.get('cloud') or '-'} / {r.get('level') or '-'}"
            f" / {d}分" if d else f"   {r.get('cloud') or '-'} / {r.get('level') or '-'} / 所要時間不明"
        )
        print(f"   {_link_str(r)}")
    return 0


def cmd_recommend(args):
    db = _ensure_db()
    conn = sqlite3.connect(db)
    try:
        records = [
            row_to_record(r)
            for r in conn.execute(
                f"SELECT {', '.join(_COLUMNS)} FROM records"
            ).fetchall()
        ]
    finally:
        conn.close()
    picked = recommend(
        records,
        minutes=args.minutes,
        interests=args.interest,
        plan_month=args.month,
        limit=args.limit,
    )
    print(format_plan(picked, minutes=args.minutes,
                      interests=args.interest, plan_month=args.month))
    return 0


def cmd_show(args):
    db = _ensure_db()
    conn = sqlite3.connect(db)
    try:
        row = conn.execute(
            f"SELECT {', '.join(_COLUMNS)} FROM records WHERE id = ?",
            (args.id,),
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        print(f"not found: {args.id}", file=sys.stderr)
        return 1
    r = row_to_record(row)
    print(f"id:          {r['id']}")
    print(f"title:       {r['title']}")
    if r.get("title_ja"):
        print(f"title_ja:    {r['title_ja']}")
    if r.get("summary_ja"):
        print(f"summary_ja:  {r['summary_ja']}")
    print(f"catalog:     {r['source_catalog']}")
    print(f"cloud:       {r.get('cloud')}")
    print(f"services:    {', '.join(r.get('services') or [])}")
    print(f"domain:      {r.get('domain')}")
    print(f"level:       {r.get('level')}")
    print(f"duration:    {r.get('duration_min')} 分" if r.get("duration_min") else "duration:    不明")
    print(f"access:      {r.get('access')}")
    print(f"priority:    {r.get('priority')}")
    print(f"plan_month:  {r.get('plan_month')}")
    print(f"link:        {_link_str(r)}")
    if r.get("related"):
        print(f"related:     {', '.join(r['related'])}")
    return 0


def cmd_stats(args):
    db = _ensure_db()
    conn = sqlite3.connect(db)
    try:
        total = conn.execute("SELECT count(*) FROM records").fetchone()[0]
        by_cat = Counter(
            r[0]
            for r in conn.execute(
                "SELECT source_catalog FROM records"
            ).fetchall()
        )
        kinds = Counter()
        for (link_json,) in conn.execute("SELECT link FROM records").fetchall():
            import json as _json

            kinds[_json.loads(link_json).get("kind")] += 1
    finally:
        conn.close()
    print(f"総レコード数: {total}")
    print("カタログ別件数:")
    for cat in sorted(by_cat):
        print(f"  {cat}: {by_cat[cat]}")
    print("link カバレッジ:")
    for kind in ("direct", "search", "none"):
        n = kinds.get(kind, 0)
        pct = 100.0 * n / total if total else 0
        print(f"  {kind}: {n} ({pct:.1f}%)")
    return 0


def cmd_export_plan(args):
    db = _ensure_db()
    conn = sqlite3.connect(db)
    try:
        records = [
            row_to_record(r)
            for r in conn.execute(
                f"SELECT {', '.join(_COLUMNS)} FROM records"
            ).fetchall()
        ]
    finally:
        conn.close()
    picked = recommend(
        records,
        minutes=args.minutes,
        interests=args.interest,
        plan_month=args.month,
        limit=args.limit,
    )
    text = "# 学習セッション計画\n\n" + format_plan(
        picked, minutes=args.minutes,
        interests=args.interest, plan_month=args.month,
    )
    out = Path(args.out)
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out}")
    return 0


def build_parser():
    p = argparse.ArgumentParser(
        prog="hands_on_search",
        description="3クラウド学習カタログの検索・推薦 CLI",
    )
    p.add_argument(
        "--db", default=str(DB_PATH),
        help="catalog.db のパス (既定: build/catalog.db)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("search", help="キーワード検索")
    s.add_argument("query", nargs="?", default="")
    s.add_argument("--cloud")
    s.add_argument("--domain")
    s.add_argument("--service")
    s.add_argument("--level")
    s.add_argument("--max-minutes", type=int, dest="max_minutes")
    s.add_argument("--access")
    s.add_argument("--priority")
    s.add_argument("--month", help="plan_month 前方一致 (例 2026-11)")
    s.add_argument("--limit", type=int, default=10)
    s.set_defaults(func=cmd_search)

    r = sub.add_parser("recommend", help="空き時間と関心から推薦")
    r.add_argument("--minutes", type=int, default=90)
    r.add_argument("--interest", nargs="+", default=[])
    r.add_argument("--month", dest="month")
    r.add_argument("--limit", type=int, default=10)
    r.set_defaults(func=cmd_recommend)

    sh = sub.add_parser("show", help="レコード詳細")
    sh.add_argument("id")
    sh.set_defaults(func=cmd_show)

    st = sub.add_parser("stats", help="カタログ別件数と link カバレッジ")
    st.set_defaults(func=cmd_stats)

    e = sub.add_parser("export-plan", help="推薦結果を Markdown 書き出し")
    e.add_argument("--minutes", type=int, default=90)
    e.add_argument("--interest", nargs="+", default=[])
    e.add_argument("--month", dest="month")
    e.add_argument("--limit", type=int, default=10)
    e.add_argument("--out", required=True)
    e.set_defaults(func=cmd_export_plan)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    global DB_PATH
    DB_PATH = Path(args.db)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
