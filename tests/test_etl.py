"""T1: 正規化ETL と URL導線のテスト"""

import json
import urllib.parse
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "data/vendor"


def test_vendor_counts(vendor_only_records):
    counts = Counter(r["source_catalog"] for r in vendor_only_records)
    assert counts == {"aws": 167, "azure": 550, "google": 176}
    assert len(vendor_only_records) == 893


def test_plan_fixture_ingested(records):
    plan = [r for r in records if r["source_catalog"] == "plan"]
    assert len(plan) == 3
    assert {r["id"] for r in plan} == {
        "plan:HO-SAMPLE-001",
        "plan:HO-SAMPLE-002",
        "plan:HO-SAMPLE-003",
    }


def test_unique_ids(records):
    ids = [r["id"] for r in records]
    assert len(ids) == len(set(ids))


def test_every_record_has_link(records):
    for r in records:
        link = r.get("link")
        assert isinstance(link, dict), r["id"]
        assert link.get("kind") in {"direct", "search", "none"}, r["id"]
        assert "url" in link and "source" in link


def _raw_url_set():
    """元データに実在する URL の集合 (捏造検出用)"""
    urls = set()

    def add(v):
        if isinstance(v, str) and v.startswith("http"):
            urls.add(v)
        elif isinstance(v, list):
            for x in v:
                add(x)

    aws = json.loads((VENDOR / "aws_builder_labs.json").read_text("utf-8"))
    for it in aws:
        add(it.get("url"))
    az = json.loads((VENDOR / "azure_learn.json").read_text("utf-8"))["items"]
    for it in az:
        add(it.get("url"))
        add(it.get("url_ja"))
    g = json.loads((VENDOR / "google_skills.json").read_text("utf-8"))
    for it in g:
        add(it.get("url"))
    plan = json.loads(
        (ROOT / "tests/fixtures/plan_sample.json").read_text("utf-8")
    )
    for it in plan:
        add(it.get("url"))
        add(it.get("reference_urls"))
    return urls


def test_no_fabricated_direct_urls(records):
    real_urls = _raw_url_set()
    for r in records:
        if r["link"]["kind"] == "direct":
            assert r["link"]["url"] in real_urls, (
                f"fabricated URL on {r['id']}: {r['link']['url']}"
            )


def test_aws_search_fallback_pattern(records):
    aws_raw = json.loads((VENDOR / "aws_builder_labs.json").read_text("utf-8"))
    no_url_titles = {
        it["title"] for it in aws_raw if not (it.get("url") or "").strip()
    }
    searched = upgraded = 0
    for r in records:
        if r["source_catalog"] != "aws" or r["title"] not in no_url_titles:
            continue
        if r["link"]["kind"] == "search":
            searched += 1
            expected = (
                "https://skillbuilder.aws/search?searchText="
                + urllib.parse.quote(r["title"])
                + "&typeId=aws_builder_lab"
            )
            assert r["link"]["url"] == expected
        elif r["link"]["kind"] == "direct":
            upgraded += 1  # T2 で direct に格上げされた件
    assert searched + upgraded == len(no_url_titles)


def test_google_no_url_records_get_search_link(records):
    """I1: 直接URLが無い Google レコード (22件) は、元データ内に実在する
    公式カタログ検索パターンで kind=search の導線を持つ。"""
    g_raw = json.loads((VENDOR / "google_skills.json").read_text("utf-8"))
    no_url_titles = {
        it["title"] for it in g_raw if not (it.get("url") or "").strip()
    }
    assert len(no_url_titles) == 22
    targets = [
        r for r in records
        if r["source_catalog"] == "google" and r["title"] in no_url_titles
    ]
    assert len(targets) == 22
    for r in targets:
        assert r["link"]["kind"] == "search"
        expected = (
            "https://www.skills.google/catalog?locale=ja&search="
            + urllib.parse.quote(r["title"])
        )
        assert r["link"]["url"] == expected


def test_google_catalog_urls_classified_as_search(records):
    """I1: /catalog へのリンクは direct ではなく検索導線なので search に分類。"""
    for r in records:
        if r["source_catalog"] != "google":
            continue
        url = r["link"].get("url") or ""
        if "/catalog" in urllib.parse.urlparse(url).path:
            assert r["link"]["kind"] == "search", r["id"]
        elif r["link"]["kind"] == "direct":
            # direct は検索ページではない実 URL のみ
            assert "/catalog" not in url


def test_google_no_none_links(vendor_only_records):
    """I1: google の none が 0 件になる。"""
    for r in vendor_only_records:
        if r["source_catalog"] == "google":
            assert r["link"]["kind"] != "none"


def test_plan_overlay_none_gets_same_treatment(records):
    """I1: plan オーバーレイで URL が無い行にも cloud 別の確認済み
    検索パターンを適用する。HO-SAMPLE-002 (Azure, URLなし) が対象。"""
    r = next(x for x in records if x["id"] == "plan:HO-SAMPLE-002")
    assert r["link"]["kind"] == "search"
    assert r["link"]["url"].startswith(
        "https://learn.microsoft.com/ja-jp/search/?terms="
    )
    assert urllib.parse.quote("サンプル") in r["link"]["url"]


def test_aws_plan_month_split(records):
    """I4: AWS の "YYYY-MM テーマ" 複合値を plan_month / plan_theme に分割。"""
    aws = [r for r in records if r["source_catalog"] == "aws"]
    split = [r for r in aws if r.get("plan_theme")]
    assert split, "分割されたレコードが無い"
    for r in split:
        assert r["plan_month"] and " " not in r["plan_month"]
        # 元の複合値は raw に残る
        assert r["plan_theme"] in (r["raw"].get("plan_month") or "")
    # 分割後は "YYYY-MM" 形式のみ (分割不能な値があれば別途確認する)
    import re

    unsplit = [
        r["plan_month"] for r in aws
        if r["plan_month"] and not re.fullmatch(r"\d{4}-\d{2}", r["plan_month"])
    ]
    assert unsplit == []


def test_azure_levels_list(records):
    """I4: Azure の複数 level 値を levels リストとして保持し、
    level (元の文字列) との後方互換を保つ。"""
    multi = [
        r for r in records
        if r["source_catalog"] == "azure" and ";" in (r["level"] or "")
    ]
    assert multi, "複数 level 値の Azure レコードが無い"
    for r in multi:
        assert r["levels"] == r["level"].split(";")
    # 単一値のレコードも levels リストを持つ
    single = next(
        r for r in records
        if r["source_catalog"] == "azure" and r["level"] == "beginner"
    )
    assert single["levels"] == ["beginner"]


def test_azure_primary_link_is_url_ja(records):
    az_raw = {
        it["uid"]: it
        for it in json.loads((VENDOR / "azure_learn.json").read_text("utf-8"))[
            "items"
        ]
    }
    for r in records:
        if r["source_catalog"] != "azure":
            continue
        raw = az_raw[r["id"].split(":", 1)[1]]
        if raw.get("url_ja"):
            assert r["link"]["kind"] == "direct"
            assert r["link"]["url"] == raw["url_ja"]
