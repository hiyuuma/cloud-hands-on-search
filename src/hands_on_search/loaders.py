"""4入力形式 (AWS / Azure / Google / plan オーバーレイ) -> 統一スキーマ"""

import json
import re
import urllib.parse
from pathlib import Path

from .normalize import normalize_services, parse_duration_minutes

AWS_SEARCH_URL = (
    "https://skillbuilder.aws/search?searchText={title}&typeId=aws_builder_lab"
)
# Google Skills の公式カタログ検索。元データの 58 レコードが実際に
# この形式の URL を持つため、実在が確認できるパターンとして採用する。
GOOGLE_SEARCH_URL = "https://www.skills.google/catalog?locale=ja&search={title}"
# Microsoft Learn の公式検索 (実在確認済み)。plan オーバーレイの Azure 行用。
AZURE_SEARCH_URL = "https://learn.microsoft.com/ja-jp/search/?terms={title}"

CLOUD_BY_CATALOG = {"aws": "AWS", "azure": "Azure", "google": "GCP"}

_SEARCH_URL_BY_CLOUD = {
    "AWS": AWS_SEARCH_URL,
    "Azure": AZURE_SEARCH_URL,
    "GCP": GOOGLE_SEARCH_URL,
}

# AWS plan_month の "2027-03 データ基盤 / 分析" 型 (月 + テーマ複合値)
_PLAN_MONTH_SPLIT = re.compile(r"^(\d{4}-\d{2})\s+(.+)$")


def _is_google_catalog_search_url(url):
    """skills.google の /catalog へのリンクはラボ本体ではなく検索結果への導線。"""
    try:
        path = urllib.parse.urlparse(url).path.rstrip("/")
    except ValueError:
        return False
    return path.endswith("/catalog")


def _search_link_for_cloud(cloud, title):
    """cloud から分かる公式検索 URL を生成する。分からなければ None。"""
    tmpl = _SEARCH_URL_BY_CLOUD.get(cloud)
    if not tmpl or not title:
        return None
    return tmpl.format(title=urllib.parse.quote(title))


def _link(url, kind, source):
    return {"url": url or "", "kind": kind, "source": source}


def _slug(text):
    """id 用の安定スラッグ (ASCII 化せず、単語をハイフン接続)"""
    s = re.sub(r"[^\w]+", "-", str(text).strip().lower(), flags=re.UNICODE)
    return s.strip("-") or "untitled"


def _base(record_id, catalog, title, raw):
    return {
        "id": record_id,
        "source_catalog": catalog,
        "title": title or "",
        "title_ja": None,
        "summary_ja": None,
        "cloud": CLOUD_BY_CATALOG.get(catalog),
        "services": [],
        "domain": None,
        "level": None,
        "levels": [],
        "duration_min": None,
        "access": None,
        "priority": None,
        "plan_month": None,
        "plan_theme": None,
        "link": _link("", "none", catalog),
        "related": [],
        "raw": raw,
    }


def normalize_aws(item):
    title = item.get("title", "")
    rec = _base("aws:" + _slug(title), "aws", title, item)
    rec["summary_ja"] = item.get("summary_ja") or None
    rec["services"] = normalize_services(item.get("main_services"))
    rec["domain"] = item.get("domain") or None
    rec["level"] = item.get("level") or None
    rec["duration_min"] = parse_duration_minutes(item.get("duration"))
    rec["access"] = item.get("access") or None
    rec["priority"] = item.get("priority_for_user") or None
    # I4: "2027-03 データ基盤 / 分析" のような月+テーマ複合値を分割する。
    # 分割できない形式は推測せずそのまま plan_month に保持する。
    raw_month = (item.get("plan_month") or "").strip()
    m = _PLAN_MONTH_SPLIT.match(raw_month)
    if m:
        rec["plan_month"], rec["plan_theme"] = m.group(1), m.group(2)
    else:
        rec["plan_month"] = raw_month or None
    url = (item.get("url") or "").strip()
    if url:
        rec["link"] = _link(url, "direct", "aws")
    else:
        search = AWS_SEARCH_URL.format(title=urllib.parse.quote(title))
        rec["link"] = _link(search, "search", "aws")
    return rec


def normalize_azure(item):
    uid = item.get("uid") or _slug(item.get("title", ""))
    rec = _base("azure:" + uid, "azure", item.get("title", ""), item)
    rec["title_ja"] = item.get("title_ja") or None
    rec["summary_ja"] = item.get("summary_ja") or item.get("summary") or None
    rec["services"] = normalize_services(item.get("main_services"))
    rec["domain"] = item.get("domain") or None
    # I4: "intermediate;advanced" のような複数値を levels リストとして保持。
    # level には元の文字列を残す (後方互換)。
    raw_levels = item.get("levels") or None
    rec["level"] = raw_levels
    if raw_levels:
        rec["levels"] = [
            s.strip() for s in str(raw_levels).split(";") if s.strip()
        ]
    rec["duration_min"] = parse_duration_minutes(item.get("duration_in_minutes"))
    rec["priority"] = item.get("priority_for_user") or None
    rec["plan_month"] = item.get("plan_month") or None
    rec["plan_theme"] = item.get("plan_theme") or None
    url_ja = (item.get("url_ja") or "").strip()
    url = (item.get("url") or "").strip()
    if url_ja:
        rec["link"] = _link(url_ja, "direct", "azure")
    elif url:
        rec["link"] = _link(url, "direct", "azure")
    return rec


def normalize_google(item):
    title = item.get("title", "")
    rec = _base("google:" + _slug(title), "google", title, item)
    rec["summary_ja"] = item.get("summary_ja") or None
    rec["services"] = normalize_services(item.get("main_services"))
    rec["domain"] = item.get("domain") or None
    rec["level"] = item.get("level") or None
    rec["duration_min"] = parse_duration_minutes(item.get("duration"))
    credits = (item.get("credits") or "").strip()
    rec["access"] = credits if credits else None
    rec["priority"] = item.get("priority_for_user") or None
    rec["plan_month"] = item.get("plan_month") or item.get("plan_month_hint") or None
    url = (item.get("url") or "").strip()
    if url:
        # /catalog へのリンクは検索結果への導線であり direct ではない
        kind = "search" if _is_google_catalog_search_url(url) else "direct"
        rec["link"] = _link(url, kind, "google")
    else:
        # 元データ内に実在する公式カタログ検索パターンで search 導線を生成
        rec["link"] = _link(
            GOOGLE_SEARCH_URL.format(title=urllib.parse.quote(title)),
            "search",
            "google",
        )
    return rec


# Run 4 追加分 (HashiCorp / Linux Foundation / GitHub Skills / Oracle) は
# 3クラウド外のカタログのため cloud は「その他」に統一する (元の値は raw に残る)。
_OTHER_CLOUD = "その他"


def _lf_access(price_text):
    """Linux Foundation: price_text の有無で課金を判定する。

    "$0" / "Free" 表記は無料、"$<正>" は有料、空欄は不明 (推測しない)。
    価格原文は raw.price_text に残る。
    """
    p = (price_text or "").strip()
    if not p:
        return "unknown"
    if p.lower() == "free":
        return "Free"
    try:
        amount = float(p.lstrip("$").replace(",", ""))
    except ValueError:
        return "unknown"
    return "Free" if amount == 0 else "Paid"


def _normalize_staged(item, catalog, record_id, access):
    """Run 4 の staging 形式カタログ共通の正規化。

    全レコードが実在確認済みの直接 URL を持つため link は常に direct。
    level は出典の値をそのまま保持し、空欄は推測しない。
    """
    rec = _base(record_id, catalog, item.get("title", ""), item)
    rec["cloud"] = _OTHER_CLOUD
    rec["summary_ja"] = item.get("summary_ja") or None
    rec["services"] = normalize_services(item.get("services"))
    rec["domain"] = item.get("domain") or None
    raw_level = item.get("level") or None
    rec["level"] = raw_level
    if raw_level:
        rec["levels"] = [
            s.strip() for s in str(raw_level).split(";") if s.strip()
        ]
    rec["duration_min"] = parse_duration_minutes(item.get("duration_text"))
    rec["access"] = access
    rec["priority"] = item.get("priority_for_user") or None
    rec["link"] = _link((item.get("url") or "").strip(), "direct", catalog)
    return rec


def normalize_hashicorp(item):
    """HashiCorp チュートリアルは全件無料。同名タイトルが製品横断で
    存在するため、一意な URL パスから ID を取る。"""
    path = urllib.parse.urlparse(item.get("url") or "").path
    rid = "hashicorp:" + _slug(path or item.get("title", ""))
    return _normalize_staged(item, "hashicorp", rid, "Free")


def normalize_linux_foundation(item):
    rid = "linux_foundation:" + _slug(item.get("title", ""))
    return _normalize_staged(
        item, "linux_foundation", rid, _lf_access(item.get("price_text"))
    )


def normalize_github_skills(item):
    """GitHub Skills のインタラクティブコースは全件無料。"""
    rid = "github_skills:" + _slug(item.get("title", ""))
    return _normalize_staged(item, "github_skills", rid, "Free")


def normalize_oracle(item):
    """Oracle MyLearn ラーニングパスと LiveLabs ワークショップは全件無料
    (収集報告 reports/catalog-expansion/oracle.md の出典確認に基づく)。"""
    rid = "oracle:" + _slug(item.get("title", ""))
    return _normalize_staged(item, "oracle", rid, "Free")


def normalize_plan(item):
    pid = item.get("id") or _slug(item.get("title", ""))
    rec = _base("plan:" + str(pid), "plan", item.get("title", ""), item)
    rec["summary_ja"] = item.get("notes") or None
    rec["cloud"] = item.get("cloud") or None
    rec["services"] = normalize_services(item.get("services") or item.get("service"))
    rec["domain"] = item.get("category") or None
    rec["duration_min"] = parse_duration_minutes(item.get("duration_estimate"))
    rec["access"] = item.get("billing_risk") or None
    rec["priority"] = item.get("priority") or None
    rec["plan_month"] = item.get("month_id") or None
    rec["plan_theme"] = item.get("monthly_theme") or None
    url = (item.get("url") or "").strip()
    if url:
        rec["link"] = _link(url, "direct", "plan")
    else:
        # I1: vendor 側と同じ扱い。cloud が分かれば確認済みの公式検索
        # パターンで search 導線を生成し、分からなければ none のままにする。
        search_url = _search_link_for_cloud(rec["cloud"], rec["title"])
        if search_url:
            rec["link"] = _link(search_url, "search", rec["cloud"].lower())
    return rec


def load_aws(path):
    items = json.loads(Path(path).read_text(encoding="utf-8"))
    return [normalize_aws(it) for it in items]


def load_azure(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    items = data["items"] if isinstance(data, dict) else data
    return [normalize_azure(it) for it in items]


def load_google(path):
    items = json.loads(Path(path).read_text(encoding="utf-8"))
    return [normalize_google(it) for it in items]


def load_hashicorp(path):
    items = json.loads(Path(path).read_text(encoding="utf-8"))
    return [normalize_hashicorp(it) for it in items]


def load_linux_foundation(path):
    items = json.loads(Path(path).read_text(encoding="utf-8"))
    return [normalize_linux_foundation(it) for it in items]


def load_github_skills(path):
    items = json.loads(Path(path).read_text(encoding="utf-8"))
    return [normalize_github_skills(it) for it in items]


def load_oracle(path):
    items = json.loads(Path(path).read_text(encoding="utf-8"))
    return [normalize_oracle(it) for it in items]


def load_plan(path):
    items = json.loads(Path(path).read_text(encoding="utf-8"))
    return [normalize_plan(it) for it in items]
