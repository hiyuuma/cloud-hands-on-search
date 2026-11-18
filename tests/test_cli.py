"""T5: CLI のテスト"""

from pathlib import Path

import pytest

from hands_on_search.cli import main
from hands_on_search.db import build_db


@pytest.fixture(scope="module")
def db(tmp_path_factory, records):
    path = tmp_path_factory.mktemp("clidb") / "catalog.db"
    build_db(records, path)
    return str(path)


def test_search_cli(db, capsys):
    assert main(["--db", db, "search", "Fargate"]) == 0
    out = capsys.readouterr().out
    assert "件ヒット" in out
    assert "http" in out  # URL 導線が表示される


def test_search_cli_filter(db, capsys):
    assert main(["--db", db, "search", "Kubernetes",
                 "--cloud", "Azure", "--limit", "5"]) == 0
    out = capsys.readouterr().out
    assert "Azure" in out


def test_recommend_cli(db, capsys):
    assert main(["--db", db, "recommend", "--minutes", "90",
                 "--interest", "MCP", "コンテナ"]) == 0
    out = capsys.readouterr().out
    assert "今日の流れ" in out
    assert "課金の見立て" in out
    assert "http" in out


def test_show_cli(db, capsys):
    assert main(["--db", db, "show",
                 "aws:deploy-and-scale-containerized-applications-with-aws-fargate"]) == 0
    out = capsys.readouterr().out
    assert "AWS Fargate" in out
    assert "link:" in out and "http" in out


def test_show_not_found(db, capsys):
    assert main(["--db", db, "show", "no:such-id"]) == 1
    assert "not found" in capsys.readouterr().err


def test_stats_cli(db, capsys):
    assert main(["--db", db, "stats"]) == 0
    out = capsys.readouterr().out
    assert "aws: 167" in out
    assert "azure: 550" in out
    assert "google: 176" in out
    assert "plan: 3" in out
    assert "direct" in out


def test_export_plan_cli(db, tmp_path, capsys):
    out_file = tmp_path / "plan.md"
    assert main(["--db", db, "export-plan", "--minutes", "90",
                 "--interest", "MCP", "--out", str(out_file)]) == 0
    text = out_file.read_text(encoding="utf-8")
    assert "今日の流れ" in text
    # 全タイトルがリンク (URL 導線仕様): 番号付き行はすべて [title](url) 形式
    import re

    numbered = [l for l in text.splitlines() if re.match(r"^\d+\. ", l)]
    assert numbered
    assert all(re.match(r"^\d+\. \[.+\]\(", l) for l in numbered)
    # URL があるものは直接リンクになっている (kind=none は "(URL なし)" 表記)
    assert "](" in text and "http" in text
