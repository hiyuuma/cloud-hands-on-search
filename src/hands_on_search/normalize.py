"""正規化ヘルパー: duration・services・タイトル"""

import re
import unicodedata

_DUR_TOKEN = re.compile(
    r"(\d+(?:\.\d+)?)\s*(hours?|hrs?|h|minutes?|mins?|m)\b",
    re.IGNORECASE,
)


def parse_duration_minutes(value):
    """'1h', '1h 30m', '45 minutes', '1 hour', '43' 等を分に変換する。

    不明・空欄は None。推測で埋めない。
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value) if value else None
    s = str(value).strip()
    if not s:
        return None
    # 純粋な数値 (Azure duration_in_minutes 等) はそのまま分とみなす
    if re.fullmatch(r"\d+(?:\.\d+)?", s):
        return int(float(s))
    total = 0.0
    matched = False
    for amount, unit in _DUR_TOKEN.findall(s):
        matched = True
        n = float(amount)
        u = unit.lower()
        total += n * 60 if u.startswith(("h", "hr")) else n
    if not matched:
        return None
    return int(round(total))


def normalize_services(value):
    """main_services 等を文字列リストに正規化する。

    'AWS Glue; Amazon Athena' -> ['AWS Glue', 'Amazon Athena']
    すでにリストなら各要素を strip して返す。
    """
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    parts = re.split(r"[;,]", str(value))
    return [p.strip() for p in parts if p.strip()]


_WS = re.compile(r"\s+")
_NON_WORD = re.compile(r"[^\w]+", re.UNICODE)


def normalize_title(title):
    """突合用のタイトル正規化キーを返す。

    - Unicode NFKC 正規化 (全角/半角ゆれの吸収)
    - 小文字化
    - 記号・空白の統一 (単語境界のみ残す)
    """
    if not title:
        return ""
    s = unicodedata.normalize("NFKC", str(title)).lower()
    s = _NON_WORD.sub(" ", s)
    return _WS.sub(" ", s).strip()


def normalize_url(url):
    """突合用の URL 正規化 (末尾スラッシュ・クエリの細差を吸収)。"""
    if not url:
        return ""
    s = str(url).strip().lower()
    s = s.split("#", 1)[0]
    return s.rstrip("/")
