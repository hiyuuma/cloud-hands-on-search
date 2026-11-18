"""4入力形式 (AWS / Azure / Google / plan オーバーレイ) -> 統一スキーマ"""

import json
import re
import urllib.parse
from pathlib import Path

from .normalize import normalize_services, parse_duration_minutes

AWS_SEARCH_URL = (
    "https://skillbuilder.aws/search?searchText={title}&typeId=aws_builder_lab"
)

CLOUD_BY_CATALOG = {"aws": "AWS", "azure": "Azure", "google": "GCP"}


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
    rec["plan_month"] = item.get("plan_month") or None
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
    rec["level"] = item.get("levels") or None
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
        rec["link"] = _link(url, "direct", "google")
    # 直接URLが無く、確実な公式検索パターンも無いため kind=none のまま (捏造しない)
    return rec


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


def load_plan(path):
    items = json.loads(Path(path).read_text(encoding="utf-8"))
    return [normalize_plan(it) for it in items]
