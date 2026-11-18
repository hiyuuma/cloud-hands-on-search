"""T3: 全文検索 + 絞り込み + ランキング。

- SQLite FTS5 (trigram) で title / title_ja / summary_ja / services / domain を検索
- trigram は3文字未満のクエリをマッチできないため、その場合は LIKE 部分一致に
  フォールバックする
- ランキングは決定的: タイトル一致を要約一致より重くし、同点は bm25 → id 順

公開関数:
    search(conn_or_path, query, **filters) -> list[dict]
"""

import sqlite3
from pathlib import Path

from .db import _COLUMNS, row_to_record

_FILTERS = (
    "cloud", "domain", "service", "level",
    "max_duration_min", "access", "priority", "plan_month",
)


def _connect(db):
    if isinstance(db, (str, Path)):
        return sqlite3.connect(db), True
    return db, False


def _row_to_record(row):
    return row_to_record(row)


def _fts_match_sql(query):
    """FTS5 MATCH 式。クエリ中の FTS 特殊文字を無効化するため各トークンを
    ダブルクォートし AND で結ぶ (空白区切り = 全語一致)。"""
    terms = [t for t in query.replace('"', " ").split() if t]
    if not terms:
        return None
    return " AND ".join(f'"{t}"' for t in terms)


def _like_candidates(conn, query):
    """3文字未満クエリ用の LIKE フォールバック。全トークンの部分一致 (AND)。"""
    terms = [t for t in query.split() if t]
    if not terms:
        return []
    conds, params = [], []
    for t in terms:
        like = f"%{t}%"
        conds.append(
            "(title LIKE ? OR title_ja LIKE ? OR summary_ja LIKE ?"
            " OR services LIKE ? OR domain LIKE ?)"
        )
        params += [like] * 5
    sql = (
        f"SELECT {', '.join(_COLUMNS)} FROM records WHERE "
        + " AND ".join(conds)
    )
    return [_row_to_record(r) for r in conn.execute(sql, params).fetchall()]


def _fts_candidates(conn, query):
    """FTS5 で候補を取り、各カラムのマッチスコア付きで返す。

    bm25(records_fts) は小さいほど良い。title 系ヒットにはボーナスを与えて
    「タイトル一致 > 要約一致」の順にする。
    """
    match = _fts_match_sql(query)
    if match is None:
        return []

    # title ヒット判定: 全トークンが title/title_ja 列にヒットするか
    # (列スコープの MATCH 式を AND で結ぶ)
    terms = [t for t in query.replace('"', " ").split() if t]
    title_match = " AND ".join("{title title_ja} : \"" + t + '"' for t in terms)
    title_ids = {
        row[0]
        for row in conn.execute(
            "SELECT id FROM records_fts WHERE records_fts MATCH ?",
            [title_match],
        ).fetchall()
    }
    rows = conn.execute(
        "SELECT r.*, bm25(records_fts) AS bm "
        "FROM records_fts JOIN records r ON r.id = records_fts.id "
        "WHERE records_fts MATCH ?",
        [match],
    ).fetchall()
    out = []
    for row in rows:
        rec = _row_to_record(row[: len(_COLUMNS)])
        rec["_bm25"] = row[-1]
        rec["_title_hit"] = rec["id"] in title_ids
        out.append(rec)
    return out


def _apply_filters(records, f):
    def ok(r):
        if f.get("cloud") and (r.get("cloud") or "").lower() != f["cloud"].lower():
            return False
        if f.get("domain") and f["domain"].lower() not in (r.get("domain") or "").lower():
            return False
        if f.get("service") and not any(
            f["service"].lower() in s.lower() for s in (r.get("services") or [])
        ):
            return False
        if f.get("level") and f["level"].lower() not in (r.get("level") or "").lower():
            return False
        if f.get("max_duration_min") is not None:
            d = r.get("duration_min")
            if d is None or d > f["max_duration_min"]:
                return False
        if f.get("access") and f["access"].lower() not in (r.get("access") or "").lower():
            return False
        if f.get("priority") and (r.get("priority") or "") != f["priority"]:
            return False
        # plan_month は "2027-03 データ基盤 / 分析" のような複合値があり得るため
        # 前方一致で月だけ指定しても拾えるようにする
        if f.get("plan_month") and not (r.get("plan_month") or "").startswith(
            f["plan_month"]
        ):
            return False
        return True

    return [r for r in records if ok(r)]


def _search_text(r):
    return " ".join(
        str(r.get(k) or "")
        for k in ("title", "title_ja", "summary_ja", "domain")
    ) + " " + " ".join(r.get("services") or [])


def search(db, query, *, limit=10, **filters):
    """キーワード検索 + 絞り込み。返り値は統一スキーマの dict のリスト。

    query が空の場合は絞り込みのみで全件 (limit まで) を返す。
    """
    unknown = set(filters) - set(_FILTERS)
    if unknown:
        raise ValueError(f"unknown filters: {sorted(unknown)}")

    conn, owned = _connect(db)
    try:
        if query and query.strip():
            terms = [t for t in query.split() if t]
            if all(len(t) >= 3 for t in terms):
                try:
                    cands = _fts_candidates(conn, query)
                except sqlite3.OperationalError:
                    cands = []
            else:
                cands = _like_candidates(conn, query)
                for r in cands:
                    r["_bm25"] = 0.0
                    r["_title_hit"] = any(
                        t.lower() in (r.get("title") or "").lower()
                        or t.lower() in (r.get("title_ja") or "").lower()
                        for t in terms
                    )
            # FTS が0件でも (トークン化の揺れで) LIKE にフォールバックして救う
            if not cands:
                cands = _like_candidates(conn, query)
                for r in cands:
                    r["_bm25"] = 0.0
                    tl = (r.get("title") or "") + " " + (r.get("title_ja") or "")
                    r["_title_hit"] = all(t.lower() in tl.lower() for t in terms)
        else:
            rows = conn.execute(
                f"SELECT {', '.join(_COLUMNS)} FROM records"
            ).fetchall()
            cands = [_row_to_record(r) for r in rows]
            for r in cands:
                r["_bm25"] = 0.0
                r["_title_hit"] = False

        cands = _apply_filters(cands, filters)
        # 決定的ランキング: タイトル一致 > bm25 (小さい方が良い) > id
        cands.sort(key=lambda r: (not r["_title_hit"], r["_bm25"], r["id"]))
        for r in cands:
            r.pop("_bm25", None)
            r.pop("_title_hit", None)
        return cands[:limit]
    finally:
        if owned:
            conn.close()
