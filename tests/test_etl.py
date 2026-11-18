"""T1: 正規化ETL と URL導線のテスト"""

import json
import urllib.parse
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "data/vendor"


def test_vendor_counts(vendor_only_records):
    counts = Counter(r["source_catalog"] for r in vendor_only_records)
    assert counts == {
        "aws": 167,
        "azure": 550,
        "google": 176,
        "hashicorp": 499,
        "linux_foundation": 59,
        "github_skills": 42,
        "oracle": 89,
    }
    assert len(vendor_only_records) == 1582


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
    # Run 4 追加カタログ: 全レコードが直接 URL を持つ
    for name in (
        "hashicorp", "linux_foundation", "github_skills", "oracle_oci"
    ):
        items = json.loads((VENDOR / f"{name}.json").read_text("utf-8"))
        for it in items:
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


# ---- Run 4: 新規4カタログ (hashicorp / linux_foundation / github_skills /
#      oracle) の統合 ----

NEW_CATALOGS = ("hashicorp", "linux_foundation", "github_skills", "oracle")


def test_new_catalogs_all_direct_links(vendor_only_records):
    """staging 由来の4カタログは全件 kind=direct (実在確認済み URL)。"""
    for r in vendor_only_records:
        if r["source_catalog"] in NEW_CATALOGS:
            assert r["link"]["kind"] == "direct", r["id"]
            assert r["link"]["url"].startswith("http"), r["id"]
            assert r["link"]["source"] == r["source_catalog"]


def test_hashicorp_unique_ids_via_url_path(vendor_only_records):
    """hashicorp は同名タイトルが製品横断・コレクション間で重複するため、
    一意な URL パス由来の ID を使う。"""
    hc = [
        r for r in vendor_only_records
        if r["source_catalog"] == "hashicorp"
    ]
    ids = [r["id"] for r in hc]
    assert len(ids) == len(set(ids)) == 499
    assert all(i.startswith("hashicorp:") for i in ids)


def test_new_catalog_common_fields(vendor_only_records):
    """title/services/priority/summary_ja が staging の値を尊重している。"""
    for r in vendor_only_records:
        if r["source_catalog"] not in NEW_CATALOGS:
            continue
        raw = r["raw"]
        assert r["title"] == raw["title"]
        assert r["priority"] == (raw.get("priority_for_user") or None)
        assert r["summary_ja"] == (raw.get("summary_ja") or None)
        assert r["services"] == raw.get("services") or []
        assert r["cloud"] == "その他"


def test_new_catalog_duration_conversion(vendor_only_records):
    """duration_text -> duration_min の代表変換と、空欄が None になること。"""
    by_cat = {}
    for r in vendor_only_records:
        by_cat.setdefault(r["source_catalog"], []).append(r)

    hc = {(r["raw"].get("duration_text") or ""): r["duration_min"]
          for r in by_cat["hashicorp"]}
    assert hc["19min"] == 19
    assert hc["1hr 30min"] == 90
    assert hc[""] is None

    oc = {(r["raw"].get("duration_text") or ""): r["duration_min"]
          for r in by_cat["oracle"]}
    assert oc["26h 30m"] == 1590
    assert oc["1 hour, 30 minutes"] == 90
    assert oc["2 hours, 15 minutes"] == 135
    assert oc["45 minutes"] == 45
    assert oc["3 hours"] == 180

    gh = {(r["raw"].get("duration_text") or ""): r["duration_min"]
          for r in by_cat["github_skills"]}
    assert gh["less than 30 minutes"] == 30
    assert gh["less than one hour"] == 60
    assert gh["less than an hour"] == 60
    assert gh["90–120 minutes"] == 120  # レンジ表記は上限を採用
    assert gh[""] is None


def test_linux_foundation_access_from_price(records):
    """LF は price_text から access を判定: $0/Free→Free, 正の価格→Paid,
    空欄→unknown (価格原文は raw に残る)。"""
    lf = [r for r in records if r["source_catalog"] == "linux_foundation"]
    assert len(lf) == 59
    for r in lf:
        price = (r["raw"].get("price_text") or "").strip()
        if not price:
            assert r["access"] == "unknown", r["id"]
        elif price in ("$0", "Free"):
            assert r["access"] == "Free", r["id"]
        else:
            assert r["access"] == "Paid", r["id"]
            assert r["raw"]["price_text"] == price  # 原文保持


def test_other_new_catalogs_free(records):
    """HashiCorp チュートリアル / GitHub Skills / Oracle MyLearn・LiveLabs
    は無料が出典確認済みのため access=Free。"""
    for r in records:
        if r["source_catalog"] in ("hashicorp", "github_skills", "oracle"):
            assert r["access"] == "Free", r["id"]


def test_new_catalog_duration_coverage(vendor_only_records):
    """変換不能 (非空だが分に直せない表記) の件数を固定する。
    現状は LF の "1 day of Instructor-led class time" 2件のみ。"""
    unconvertible = {}
    empty = {}
    for r in vendor_only_records:
        if r["source_catalog"] not in NEW_CATALOGS:
            continue
        cat = r["source_catalog"]
        text = (r["raw"].get("duration_text") or "").strip()
        if not text:
            empty[cat] = empty.get(cat, 0) + 1
        elif r["duration_min"] is None:
            unconvertible.setdefault(cat, []).append(text)
    assert unconvertible == {
        "linux_foundation": [
            "1 day of Instructor-led class time",
            "1 day of Instructor-led class time",
        ]
    }
    assert empty == {
        "hashicorp": 22,
        "linux_foundation": 54,
        "github_skills": 2,
        "oracle": 15,
    }
