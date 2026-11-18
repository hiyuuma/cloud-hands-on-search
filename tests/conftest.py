import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hands_on_search.etl import run_etl  # noqa: E402

FIXTURE_PLAN = ROOT / "tests/fixtures/plan_sample.json"


@pytest.fixture(scope="session")
def records(tmp_path_factory):
    """vendor 3カタログ + plan フィクスチャで ETL を1回だけ実行する。"""
    build_dir = tmp_path_factory.mktemp("build")
    recs, report, _ = run_etl(
        paths={"plan": FIXTURE_PLAN}, build_dir=build_dir, write_outputs=False
    )
    return recs


@pytest.fixture(scope="session")
def vendor_only_records(tmp_path_factory):
    build_dir = tmp_path_factory.mktemp("build_vendor")
    recs, _, _ = run_etl(
        paths={"plan": None}, build_dir=build_dir, write_outputs=False
    )
    return recs
