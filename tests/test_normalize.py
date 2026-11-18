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
