"""SQLite データ層。T3 の FTS5 検索の土台となる records テーブルを提供する。

DB ファイルは生成物 (git 対象外)。build_db() で再生成できる。
"""

import json
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS records (
    id TEXT PRIMARY KEY,
    source_catalog TEXT NOT NULL,
    title TEXT NOT NULL,
    title_ja TEXT,
    summary_ja TEXT,
    cloud TEXT,
    services TEXT NOT NULL,      -- JSON array
    domain TEXT,
    level TEXT,
    levels TEXT,               -- JSON array (複数 level 値。I4)
    duration_min INTEGER,
    access TEXT,
    priority TEXT,
    plan_month TEXT,
    plan_theme TEXT,
    link TEXT NOT NULL,          -- JSON {url, kind, source}
    link_lang TEXT,              -- リンク先ページの言語 "ja"/"en" (Run 6)
    related TEXT NOT NULL,       -- JSON array of ids
    raw TEXT NOT NULL            -- JSON original record
);
CREATE INDEX IF NOT EXISTS idx_records_catalog ON records(source_catalog);
CREATE INDEX IF NOT EXISTS idx_records_cloud ON records(cloud);

-- T3: FTS5 trigram 全文検索。日本語の部分一致を効かせるため trigram を使う
-- (unicode61 等のトークナイザは日本語の単語分割ができず実質全文一致になる)。
-- services は検索対象に含めるため JSON ではなく空白区切りテキストで入れる。
CREATE VIRTUAL TABLE IF NOT EXISTS records_fts USING fts5(
    id UNINDEXED,
    title,
    title_ja,
    summary_ja,
    services,
    domain,
    tokenize = 'trigram'
);
"""

_COLUMNS = [
    "id", "source_catalog", "title", "title_ja", "summary_ja", "cloud",
    "services", "domain", "level", "levels", "duration_min", "access", "priority",
    "plan_month", "plan_theme", "link", "link_lang", "related", "raw",
]

_JSON_COLUMNS = {"services", "levels", "link", "related", "raw"}


def record_to_row(rec):
    return tuple(
        json.dumps(rec.get(c), ensure_ascii=False) if c in _JSON_COLUMNS else rec.get(c)
        for c in _COLUMNS
    )


def row_to_record(row):
    rec = dict(zip(_COLUMNS, row))
    for c in _JSON_COLUMNS:
        rec[c] = json.loads(rec[c])
    return rec


def build_db(records, path):
    """records を SQLite に書き出す。path の親ディレクトリは自動作成。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    try:
        conn.executescript(SCHEMA)
        conn.executemany(
            f"INSERT INTO records ({', '.join(_COLUMNS)}) "
            f"VALUES ({', '.join('?' * len(_COLUMNS))})",
            [record_to_row(r) for r in records],
        )
        conn.executemany(
            "INSERT INTO records_fts (id, title, title_ja, summary_ja,"
            " services, domain) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (
                    r["id"],
                    r.get("title") or "",
                    r.get("title_ja") or "",
                    r.get("summary_ja") or "",
                    " ".join(r.get("services") or []),
                    r.get("domain") or "",
                )
                for r in records
            ],
        )
        conn.commit()
    finally:
        conn.close()
    return path


def load_db(path):
    conn = sqlite3.connect(path)
    try:
        rows = conn.execute(
            f"SELECT {', '.join(_COLUMNS)} FROM records ORDER BY id"
        ).fetchall()
        return [row_to_record(r) for r in rows]
    finally:
        conn.close()
