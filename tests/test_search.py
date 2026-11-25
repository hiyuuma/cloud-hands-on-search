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


# Run 4: 新規カタログを対象にしたゴールデンクエリ追加検証

def test_golden_terraform_hashicorp_top(db):
    """Terraform で HashiCorp 公式チュートリアルが上位に来る。"""
    res = search(db, "Terraform", limit=10)
    hc = [r for r in res if r["source_catalog"] == "hashicorp"]
    assert hc, _titles(res)
    assert hc[0]["link"]["kind"] == "direct"
    assert "developer.hashicorp.com" in hc[0]["link"]["url"]


def test_golden_kubernetes_linux_foundation(db):
    """Kubernetes で Linux Foundation のコースがヒットする。"""
    res = search(db, "Kubernetes", limit=10)
    assert any(
        r["source_catalog"] == "linux_foundation" for r in res
    ), _titles(res)


def test_golden_mcp_livelabs(db):
    """MCP で LiveLabs の "Put AI Agents to Work with MCP" がヒットする。"""
    res = search(db, "MCP", limit=100)
    assert any(
        r["source_catalog"] == "oracle"
        and "Put AI Agents to Work with MCP" in (r["title"] or "")
        for r in res
    ), _titles(res)


# Run 5: 新規カタログを対象にしたゴールデンクエリ追加検証

def test_golden_langgraph_langchain(db):
    """LangGraph で LangChain Academy のコースがヒットする。"""
    res = search(db, "LangGraph", limit=10)
    assert any(
        r["source_catalog"] == "langchain" for r in res
    ), _titles(res)


def test_golden_sql_injection_portswigger(db):
    """SQLインジェクションで PortSwigger のトピックがヒットする。"""
    res = search(db, "SQL injection", limit=10)
    assert any(
        r["source_catalog"] == "portswigger" for r in res
    ), _titles(res)


def test_golden_kubernetes_redhat(db):
    """Kubernetes で Red Hat Developer のラーニングパスがヒットする。"""
    # "Learn Kubernetes using the Developer Sandbox" は実測で31位のため
    # limit=50 でヒットを確認する (多数の HashiCorp 教材が上位を占める)
    res = search(db, "Kubernetes", limit=50)
    assert any(
        r["source_catalog"] == "redhat" for r in res
    ), _titles(res)


def test_golden_fortiauthenticator_fortinet(db):
    """FortiAuthenticator で Fortinet のコースがヒットする。"""
    res = search(db, "FortiAuthenticator", limit=10)
    assert res and any(
        r["source_catalog"] == "fortinet" for r in res
    ), _titles(res)


def test_golden_nextjs_learn(db):
    """Next.js で Next.js Learn のコースがヒットする。"""
    res = search(db, "Next.js", limit=10)
    assert any(
        r["source_catalog"] == "nextjs" for r in res
    ), _titles(res)


def test_golden_fde_palantir(db):
    """Run 8: "FDE" で Palantir Learn のコースがヒットする。"""
    res = search(db, "FDE", limit=25)
    assert any(
        r["source_catalog"] == "palantir" for r in res
    ), _titles(res)


def test_golden_mcp_multi_catalog(db):
    """Run 8: "MCP" が複数カタログ (microsoft_curricula / cloudflare /
    anthropic / deeplearning_ai / huggingface) に跨ってヒットする。"""
    res = search(db, "MCP", limit=100)
    cats = {r["source_catalog"] for r in res}
    for expected in (
        "microsoft_curricula", "cloudflare", "anthropic",
        "deeplearning_ai", "huggingface",
    ):
        assert expected in cats, f"{expected} が MCP でヒットしない {cats}"


def test_golden_openai_catalog(db):
    """Run 8: "OpenAI" で OpenAI Academy のコースがヒットする。"""
    res = search(db, "OpenAI", limit=25)
    assert any(
        r["source_catalog"] == "openai" for r in res
    ), _titles(res)


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


def _text(r):
    return " ".join(
        str(r.get(k) or "")
        for k in ("title", "title_ja", "summary_ja", "domain")
    ) + " " + " ".join(r.get("services") or [])


def test_short_query_word_boundary(db):
    # I2: "AI" は独立した語としてのみマッチし、
    # "Available"/"Availability" のような単語中の部分一致は除外する
    import re

    res = search(db, "AI", limit=500)
    assert res, "AI でヒットなし"
    bounded = re.compile(r"(?<![0-9A-Za-z])ai(?![0-9A-Za-z])", re.IGNORECASE)
    for r in res:
        assert bounded.search(_text(r)), r["title"]


def test_unknown_mode_rejected(db):
    with pytest.raises(ValueError):
        search(db, "Fargate", mode="xor")


def test_or_mode(db):
    # OR 検索は AND の結果を包含し、各語が独立にヒットする
    and_res = search(db, "Fargate PostgreSQL", mode="and", limit=500)
    or_res = search(db, "Fargate PostgreSQL", mode="or", limit=500)
    and_ids = {r["id"] for r in and_res}
    or_ids = {r["id"] for r in or_res}
    assert and_ids <= or_ids
    assert len(or_ids) > len(and_ids)
    for r in or_res:
        t = _text(r).lower()
        assert "fargate" in t or "postgresql" in t


def test_phrase_mode(db):
    # フレーズ検索は連続する文字列にのみマッチする
    res = search(db, "Kubernetes in Google Cloud", mode="phrase", limit=20)
    assert res, "フレーズでヒットなし"
    for r in res:
        assert "kubernetes in google cloud" in _text(r).lower()


def test_phrase_mode_short(db):
    # 短いフレーズも単語境界ルールで扱う ("AI" は単語中にマッチしない)
    import re

    res = search(db, "AI", mode="phrase", limit=500)
    assert res
    bounded = re.compile(r"(?<![0-9A-Za-z])ai(?![0-9A-Za-z])", re.IGNORECASE)
    assert all(bounded.search(_text(r)) for r in res)


def test_level_filter_multi_values(db):
    # I4: "intermediate;advanced" のような複数値は各要素にマッチする
    res_adv = search(db, "", level="advanced", limit=500)
    res_int = search(db, "", level="intermediate", limit=500)
    multi = next(
        r for r in res_adv
        if r["source_catalog"] == "azure" and len(r.get("levels") or []) > 1
    )
    assert "advanced" in multi["levels"]
    assert multi["id"] in {r["id"] for r in res_int}
    # level 文字列 (後方互換フィールド) も保持されている
    assert ";" in multi["level"]


# I2: ゴールデンクエリ拡充。実データに存在が確認済みの語だけを使う。
# 各タプルは (クエリ, 期待条件の説明)。
GOLDEN_QUERIES = [
    ("Fargate", "タイトルに Fargate を含むレコードが上位に来る"),
    ("MCP", "MCP をタイトル/要約に含むレコードがヒット"),
    ("PostgreSQL", "Azure Database for PostgreSQL 系がヒット"),
    ("Kubernetes", "Kubernetes をタイトル等に含むレコードがヒット"),
    ("Lambda", "Lambda を含むレコードがヒット"),
    ("VPC", "VPC を含むレコードがヒット"),
    ("IAM", "IAM を含むレコードがヒット"),
    ("Terraform", "Terraform を含むレコードがヒット"),
    ("コンテナ", "コンテナ (日本語部分一致) がヒット"),
    ("セキュリティ", "セキュリティ関連レコードがヒット"),
    ("ネットワーク", "ネットワーク関連レコードがヒット"),
    ("データベース", "データベース関連レコードがヒット"),
    ("RAG", "RAG を含むレコードがヒット"),
    ("Cloud Run", "Cloud Run を含むレコードがヒット"),
    ("AI", "短い語でも独立した語としてヒット (ノイズなし)"),
]


@pytest.mark.parametrize("query", [q for q, _ in GOLDEN_QUERIES],
                         ids=[q for q, _ in GOLDEN_QUERIES])
def test_golden_queries(db, query):
    """全ゴールデンクエリで、検索対象テキストに語を含むレコードが
    少なくとも1件ヒットすることを検証する。"""
    import re

    res = search(db, query, limit=10)
    assert res, f"{query} でヒットなし"
    if len(query) < 3:
        pat = re.compile(
            r"(?<![0-9A-Za-z])" + re.escape(query) + r"(?![0-9A-Za-z])",
            re.IGNORECASE,
        )
    else:
        pat = re.compile(re.escape(query), re.IGNORECASE)
    assert any(pat.search(_text(r)) for r in res), (
        f"{query}: 語を含む結果なし {_text(res[0])[:120]}"
    )


def test_unknown_filter_rejected(db):
    with pytest.raises(ValueError):
        search(db, "x", bogus_filter=1)
