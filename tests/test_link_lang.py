"""Run 6: link_lang (リンク先ページ言語フラグ) のテスト"""

import json
from collections import Counter
from pathlib import Path

import pytest

from hands_on_search.cli import main
from hands_on_search.db import build_db
from hands_on_search.normalize import detect_link_lang
from hands_on_search.search import search

ROOT = Path(__file__).resolve().parents[1]

# 期待値 (指示書の実測): azure 550 + anthropic 29 + google 80 + oracle 1
EXPECTED_JA_BY_CATALOG = {
    "azure": 550,
    "anthropic": 29,
    "google": 80,
    "oracle": 1,
}
EXPECTED_JA_TOTAL = 660


@pytest.fixture(scope="module")
def db(tmp_path_factory, records):
    path = tmp_path_factory.mktemp("langdb") / "catalog.db"
    build_db(records, path)
    return str(path)


# ---- detect_link_lang 単体テスト ----

@pytest.mark.parametrize(
    "url",
    [
        "https://learn.microsoft.com/ja-jp/training/modules/foo/",
        "https://academy.claude.com/ja/courses/ai-capabilities-and-limitations",
        "https://www.skills.google/catalog?locale=ja&search=Foo",
        "https://www.skills.google/catalog?hl=ja",
        "https://mylearn.oracle.com/ou/learning-path/"
        "japanese-become-an-oracle-cloud-infrastructure-security-professional-2026-/165109",
        "https://learn.microsoft.com/ja-jp/search/?terms=Foo",
    ],
)
def test_detect_link_lang_ja(url):
    assert detect_link_lang(url) == "ja"


@pytest.mark.parametrize(
    "url",
    [
        "https://learn.microsoft.com/en-us/training/modules/foo/",
        "https://academy.claude.com/courses/ai-capabilities-and-limitations",
        "https://www.skills.google/course_templates/1275",
        "https://www.skills.google/catalog?search=Foo",
        "https://skillbuilder.aws/search?searchText=Foo&typeId=aws_builder_lab",
        "https://mylearn.oracle.com/ou/learning-path/"
        "become-an-oci-foundations-associate-2026/163541",
        "https://developer.hashicorp.com/terraform/tutorials/foo",
        "",
        None,
    ],
)
def test_detect_link_lang_en(url):
    assert detect_link_lang(url) == "en"


# ---- ETL 統合テスト ----

def test_every_record_has_link_lang(records):
    for r in records:
        assert r["link_lang"] in {"ja", "en"}, r["id"]


def test_link_lang_counts_fixed(vendor_only_records):
    """ja 件数を実測値で固定する (パターン見落としの検知用)。"""
    ja = Counter(
        r["source_catalog"]
        for r in vendor_only_records
        if r["link_lang"] == "ja"
    )
    assert dict(ja) == EXPECTED_JA_BY_CATALOG
    assert sum(ja.values()) == EXPECTED_JA_TOTAL


def test_search_link_lang_filter(db):
    # records フィクスチャは plan 3件を含み、そのうち1件は
    # learn.microsoft.com/ja-jp/search への search 導線 (ja)
    ja = search(db, "", link_lang="ja", limit=3000)
    assert len(ja) == EXPECTED_JA_TOTAL + 1
    assert all(r["link_lang"] == "ja" for r in ja)
    en = search(db, "", link_lang="en", limit=3000)
    assert all(r["link_lang"] == "en" for r in en)
    assert len(ja) + len(en) == len(search(db, "", limit=3000))


def test_search_link_lang_and_kind(records):
    """kind=search の導線 URL も同じルールで判定されている。"""
    ja = [r for r in records if r["link_lang"] == "ja"]
    assert any(r["link"]["kind"] == "search" for r in ja)


def test_search_cli_lang(db, capsys):
    assert main(["--db", db, "search", "--lang", "ja",
                 "--limit", "5"]) == 0
    out = capsys.readouterr().out
    assert "件ヒット" in out
    assert "lang: ja" in out


def test_web_compact_has_link_lang():
    """web/unified-compact.json が link_lang を含む (再生成済み)。"""
    data = json.loads(
        (ROOT / "web/unified-compact.json").read_text(encoding="utf-8")
    )
    assert data
    assert all(r.get("link_lang") in {"ja", "en"} for r in data)
    ja = sum(1 for r in data if r["link_lang"] == "ja")
    assert ja == EXPECTED_JA_TOTAL
