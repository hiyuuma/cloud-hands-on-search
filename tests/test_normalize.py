"""正規化ヘルパーの単体テスト"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hands_on_search.normalize import (  # noqa: E402
    normalize_services,
    normalize_title,
    parse_duration_minutes,
)


def test_duration_representative_cases():
    assert parse_duration_minutes("1h") == 60
    assert parse_duration_minutes("1h 30m") == 90
    assert parse_duration_minutes("2h 50m") == 170
    assert parse_duration_minutes("45m") == 45
    assert parse_duration_minutes("1 hour") == 60
    assert parse_duration_minutes("45 minutes") == 45
    assert parse_duration_minutes("43") == 43  # Azure の分数値
    assert parse_duration_minutes("") is None
    assert parse_duration_minutes(None) is None


def test_duration_30_minutes():
    assert parse_duration_minutes("30 minutes") == 30


def test_normalize_services():
    assert normalize_services("AWS Glue; Amazon Athena") == [
        "AWS Glue",
        "Amazon Athena",
    ]
    assert normalize_services("a;b;c") == ["a", "b", "c"]
    assert normalize_services(["Amazon ECS", "AWS Fargate"]) == [
        "Amazon ECS",
        "AWS Fargate",
    ]
    assert normalize_services("") == []
    assert normalize_services(None) == []


def test_normalize_title():
    assert normalize_title("Deploy and Scale Containerized Applications "
                           "with AWS Fargate") == (
        "deploy and scale containerized applications with aws fargate"
    )
    # 記号・大小・全角半角ゆれ
    assert normalize_title("EC2: 入門！") == normalize_title("ec2 入門!")


def test_duration_run4_notations():
    """Run 4 staging の多様な表記 (指示書の代表例 + 実データの表記)。"""
    assert parse_duration_minutes("26h 30m") == 1590
    assert parse_duration_minutes("1 hour, 30 minutes") == 90
    assert parse_duration_minutes("2 hours, 15 minutes") == 135
    assert parse_duration_minutes("15 minutes") == 15
    assert parse_duration_minutes("3 hours") == 180
    assert parse_duration_minutes("10min") == 10
    assert parse_duration_minutes("1hr 40min") == 100
    # "less than X" は上限 X、"a/an/one hour" は 60 分
    assert parse_duration_minutes("less than 30 minutes") == 30
    assert parse_duration_minutes("less than one hour") == 60
    assert parse_duration_minutes("less than an hour") == 60
    assert parse_duration_minutes("roughly 55 minutes") == 55
    assert parse_duration_minutes("Duration of Exam 90 minutes") == 90
    # レンジ表記は後側 (上限) を採用
    assert parse_duration_minutes("90–120 minutes") == 120
    # 日単位は変換できないので None
    assert parse_duration_minutes("1 day of Instructor-led class time") is None
