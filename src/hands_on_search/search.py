"""T3/I2: 全文検索 + 絞り込み + ランキング。

- SQLite FTS5 (trigram) で title / title_ja / summary_ja / services / domain を検索
- trigram は3文字未満のクエリをマッチできないため、その場合は LIKE 部分一致に
  フォールバックする (I2: 短い語は単語境界を意識して単語中の部分一致を除く)
- 検索モード: and (既定・全語一致) / or (いずれかの語) / phrase (フレーズ一致)
- ランキングは決定的: タイトル一致を要約一致より重くし、同点は bm25 → id 順

公開関数:
    search(conn_or_path, query, mode="and"|"or"|"phrase", **filters) -> list[dict]
"""

import re
import sqlite3
from pathlib import Path

from .db import _COLUMNS, row_to_record

_FILTERS = (
    "cloud", "domain", "service", "level",
    "max_duration_min", "access", "priority", "plan_month", "link_lang",
)

_MODES = ("and", "or", "phrase")

# 短い語 (3文字未満) の単語境界: 前後が ASCII 英数字でなければ独立した語と
# みなす ("AI" は "AI Agents" や「生成AI」にマッチし、"Available" には
# マッチしない)。日本語文字は \w に含めると「生成AI」を弾いてしまうため
# ASCII 英数字だけを境界判定に使う。
_BOUNDARY = r"(?<![0-9A-Za-z]){}(?![0-9A-Za-z])"
_TERM_LEN_FOR_BOUNDARY = 3


def _connect(db):
    if isinstance(db, (str, Path)):
        return sqlite3.connect(db), True
    return db, False


def _row_to_record(row):
    return row_to_record(row)


def _terms(query, mode):
    """クエリをトークン列にする。phrase モードでは全体を1語として扱う。"""
    q = query.replace('"', " ").strip()
    if mode == "phrase":
        return [q] if q else []
    return [t for t in q.split() if t]


def _fts_match_sql(query, mode):
    """FTS5 MATCH 式。クエリ中の FTS 特殊文字を無効化するため各トークンを
    ダブルクォートし、モードに応じて AND/OR/フレーズで結ぶ。"""
    terms = _terms(query, mode)
    if not terms:
        return None
    if mode == "phrase":
        return '"' + terms[0] + '"'
    op = " OR " if mode == "or" else " AND "
    return op.join(f'"{t}"' for t in terms)


def _term_re(term):
    """短い語は単語境界、長い語は部分一致の正規表現を返す。"""
    if len(term) < _TERM_LEN_FOR_BOUNDARY:
        return re.compile(_BOUNDARY.format(re.escape(term)), re.IGNORECASE)
    return None


def _term_matches(text, term):
    """テキストに term がマッチするか (短い語は単語境界を要求)。"""
    if len(term) < _TERM_LEN_FOR_BOUNDARY:
        return bool(_term_re(term).search(text))
    return term.lower() in text.lower()


def _matches_all_terms(text, terms, mode):
    if mode == "or":
        return any(_term_matches(text, t) for t in terms)
    return all(_term_matches(text, t) for t in terms)


def _like_candidates(conn, query, mode):
    """LIKE フォールバック。SQL の部分一致で候補を取り、短い語については
    単語境界チェックで Python 側に絞り込む ("AI"→"Available" ノイズ除去)。"""
    terms = _terms(query, mode)
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
    joiner = " OR " if mode == "or" else " AND "
    sql = (
        f"SELECT {', '.join(_COLUMNS)} FROM records WHERE "
        + joiner.join(conds)
    )
    out = []
    for r in conn.execute(sql, params).fetchall():
        rec = _row_to_record(r)
        # 短い語が単語中にしか現れない候補を落とす
        if _matches_all_terms(_search_text(rec), terms, mode):
            out.append(rec)
    return out


def _fts_candidates(conn, query, mode):
    """FTS5 で候補を取り、各カラムのマッチスコア付きで返す。

    bm25(records_fts) は小さいほど良い。title 系ヒットにはボーナスを与えて
    「タイトル一致 > 要約一致」の順にする。
    """
    match = _fts_match_sql(query, mode)
    if match is None:
        return []

    # title ヒット判定: title/title_ja 列スコープの MATCH 式
    terms = _terms(query, mode)
    if mode == "phrase":
        title_match = '{title title_ja} : "' + terms[0] + '"'
    else:
        op = " OR " if mode == "or" else " AND "
        title_match = op.join("{title title_ja} : \"" + t + '"' for t in terms)
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
        # I4: levels リスト (Azure の複数値) がある場合は各要素にマッチ。
        # 無ければ従来どおり level 文字列の部分一致。
        if f.get("level"):
            lv = f["level"].lower()
            levels = r.get("levels") or []
            if levels:
                if not any(lv in el.lower() for el in levels):
                    return False
            elif lv not in (r.get("level") or "").lower():
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
        if f.get("link_lang") and (r.get("link_lang") or "") != f["link_lang"]:
            return False
        return True

    return [r for r in records if ok(r)]


def _search_text(r):
    return " ".join(
        str(r.get(k) or "")
        for k in ("title", "title_ja", "summary_ja", "domain")
    ) + " " + " ".join(r.get("services") or [])


def _needs_like_fallback(terms, mode):
    """短い語 (3文字未満) を含むか。FTS5 trigram はそれらを索引化できない。"""
    if mode == "phrase":
        return bool(terms) and len(terms[0]) < _TERM_LEN_FOR_BOUNDARY
    return any(len(t) < _TERM_LEN_FOR_BOUNDARY for t in terms)


def search(db, query, *, mode="and", limit=10, **filters):
    """キーワード検索 + 絞り込み。返り値は統一スキーマの dict のリスト。

    mode: "and" (既定・全語一致) / "or" (いずれかの語) / "phrase" (フレーズ)。
    query が空の場合は絞り込みのみで全件 (limit まで) を返す。
    """
    if mode not in _MODES:
        raise ValueError(f"unknown mode: {mode!r} (expected one of {_MODES})")
    unknown = set(filters) - set(_FILTERS)
    if unknown:
        raise ValueError(f"unknown filters: {sorted(unknown)}")

    conn, owned = _connect(db)
    try:
        if query and query.strip():
            terms = _terms(query, mode)
            if not _needs_like_fallback(terms, mode):
                try:
                    cands = _fts_candidates(conn, query, mode)
                except sqlite3.OperationalError:
                    cands = []
            else:
                cands = _like_candidates(conn, query, mode)
                for r in cands:
                    r["_bm25"] = 0.0
                    tl = (r.get("title") or "") + " " + (r.get("title_ja") or "")
                    r["_title_hit"] = _matches_all_terms(tl, terms, mode)
            # FTS が0件でも (トークン化の揺れで) LIKE にフォールバックして救う
            if not cands:
                cands = _like_candidates(conn, query, mode)
                for r in cands:
                    r["_bm25"] = 0.0
                    tl = (r.get("title") or "") + " " + (r.get("title_ja") or "")
                    r["_title_hit"] = _matches_all_terms(tl, terms, mode)
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
