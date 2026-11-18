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
