"""T3: 検索 (FTS5 + 絞り込み + ランキング) のテスト"""

import pytest

from hands_on_search.db import build_db
from hands_on_search.search import search


@pytest.fixture(scope="module")
def db(tmp_path_factory, records):
    path = tmp_path_factory.mktemp("db") / "catalog.db"
    build_db(records, path)
    return path


def _titles(results):
    return [r["title"] for r in results]


def test_golden_fargate(db):
    res = search(db, "Fargate", limit=5)
    assert any(
        t == "Deploy and Scale Containerized Applications with AWS Fargate"
        for t in _titles(res)
    ), _titles(res)


def test_golden_mcp(db):
    res = search(db, "MCP", limit=10)
    assert res, "MCP でヒットなし"
    assert any(
        "MCP" in (r["title"] or "") or "MCP" in (r["summary_ja"] or "")
        for r in res
    )


def test_golden_postgresql(db):
    res = search(db, "PostgreSQL", limit=5)
    assert any(
        "Azure Database for PostgreSQL" in t and "Configure and migrate" in t
        for t in _titles(res)
    ), _titles(res)


def test_golden_kubernetes(db):
    res = search(db, "Kubernetes", limit=10)
    assert any("Kubernetes" in t for t in _titles(res))


def test_title_match_ranks_above_summary(db):
    # "PostgreSQL" はタイトルに含むレコードが先に来るべき
    res = search(db, "PostgreSQL", limit=10)
    title_hits = [r for r in res if "PostgreSQL" in (r["title"] or "")]
    assert title_hits, _titles(res)
    assert "PostgreSQL" in (res[0]["title"] or "") or "PostgreSQL" in (
        res[0]["title_ja"] or ""
    )


def test_deterministic_order(db):
    a = _titles(search(db, "コンテナ", limit=10))
    b = _titles(search(db, "コンテナ", limit=10))
    assert a == b


def test_filters(db):
    res = search(db, "", cloud="AWS", limit=500)
    assert res and all(r["cloud"] == "AWS" for r in res)

    res = search(db, "", max_duration_min=30, limit=500)
    assert all(
        r["duration_min"] is not None and r["duration_min"] <= 30 for r in res
    )

    res = search(db, "", service="EKS", limit=500)
    assert all(
        any("eks" in s.lower() for s in r["services"]) for r in res
    )

    res = search(db, "", plan_month="2027-03", limit=500)
    assert res and all(
        (r["plan_month"] or "").startswith("2027-03") for r in res
    )


def test_results_have_links(db):
    for r in search(db, "Kubernetes", limit=10):
        assert r["link"]["kind"] in {"direct", "search", "none"}


def test_short_query_like_fallback(db):
    # 2文字クエリは trigram が効かないため LIKE フォールバック
    res = search(db, "AI", limit=10)
    assert res


def test_unknown_filter_rejected(db):
    with pytest.raises(ValueError):
        search(db, "x", bogus_filter=1)
