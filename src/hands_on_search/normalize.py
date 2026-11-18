"""正規化ヘルパー: duration・services・タイトル"""

import re
import unicodedata
import urllib.parse

_DUR_TOKEN = re.compile(
    r"(\d+(?:\.\d+)?)\s*(hours?|hrs?|h|minutes?|mins?|m)\b",
    re.IGNORECASE,
)

# "an hour" / "one hour" のような英語の数詞表現 (GitHub Skills 等で使われる)
_DUR_WORD_NUM = re.compile(
    r"\b(?:an?|one)\s+(?=(?:hours?|hrs?|minutes?|mins?)\b)",
    re.IGNORECASE,
)


def parse_duration_minutes(value):
    """'1h', '1h 30m', '45 minutes', '1 hour', '43' 等を分に変換する。

    "less than 30 minutes" は上限の 30 を返す。"90–120 minutes" のような
    レンジ表記は後側の値 (上限) を返す。"1 day ..." のような日単位や
    不明・空欄は None。推測で埋めない。
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value) if value else None
    s = str(value).strip()
    if not s:
        return None
    s = _DUR_WORD_NUM.sub("1 ", s)
    # "1,800 hours" のような桁区切りカンマを除去して数値として読む
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)
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


# link_lang 判定 (Run 6): 「収録リンク URL が指すページの言語」。
# パターンは実データで確認したものだけを使う (推測で埋めない):
#   - パスに ja ロケールのセグメント: learn.microsoft.com/ja-jp/ (azure 550),
#     academy.claude.com/ja/ (anthropic 29)
#   - クエリの locale/hl/lang=ja: skills.google ?locale=ja (google 80)
#   - oracle.com の japanese- スラグ: mylearn.oracle.com/ou/learning-path/
#     japanese-... (oracle 1)
_JA_LOCALE_SEGMENTS = {"ja", "ja-jp", "ja_jp"}
_JA_QUERY_KEYS = ("locale", "hl", "lang")


def detect_link_lang(url):
    """リンク URL が指すページの言語を決定的に判定し "ja" / "en" を返す。

    URL に日本語ロケールが明示されている場合のみ "ja"。それ以外は "en"
    (プラットフォームに日本語版が別途存在しても、収録リンクが英語ページ
    なら "en")。kind=search の検索導線 URL も同じルールで判定する。
    """
    if not url:
        return "en"
    try:
        parts = urllib.parse.urlsplit(str(url))
    except ValueError:
        return "en"
    segs = {s.lower() for s in parts.path.split("/") if s}
    if segs & _JA_LOCALE_SEGMENTS:
        return "ja"
    qs = urllib.parse.parse_qs(parts.query)
    for key in _JA_QUERY_KEYS:
        if any(v.lower().startswith("ja") for v in qs.get(key, [])):
            return "ja"
    if parts.netloc.lower().endswith("oracle.com") and any(
        s.lower().startswith("japanese-") for s in segs
    ):
        return "ja"
    return "en"
