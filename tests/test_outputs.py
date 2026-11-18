"""link_report と DB データ層のテスト"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hands_on_search.db import build_db, load_db  # noqa: E402
from hands_on_search.link_report import link_report  # noqa: E402


def test_link_report_totals(records):
    report = link_report(records)
    total = sum(c["total"] for c in report.values())
    assert total == len(records)
    kinds = {"direct", "search", "none"}
    for c in report.values():
        assert c["direct"] + c["search"] + c["none"] == c["total"]
        assert set(c) - kinds == {"total"}


def test_db_roundtrip(records, tmp_path):
    db_path = build_db(records, tmp_path / "catalog.db")
    loaded = load_db(db_path)
    assert len(loaded) == len(records)
    sample = next(r for r in loaded if r["id"] == "plan:HO-SAMPLE-003")
    assert sample["link"]["kind"] in {"direct", "search", "none"}
    assert isinstance(sample["services"], list)
