"""ETL パイプライン本体。

vendor 3カタログ + ローカル plan オーバーレイを読み込み、統一スキーマに
正規化し、T2 横断リンクを付けて build/ に書き出す。

    python3 -m hands_on_search.etl            # build/unified.json 等を生成
"""

import json
import sys
from pathlib import Path

from .db import build_db
from .link_report import link_report, link_report_markdown
from .loaders import load_aws, load_azure, load_google, load_plan
from .related import build_related

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_PATHS = {
    "aws": REPO_ROOT / "data/vendor/aws_builder_labs.json",
    "azure": REPO_ROOT / "data/vendor/azure_learn.json",
    "google": REPO_ROOT / "data/vendor/google_skills.json",
    "plan": REPO_ROOT / "data/local/plan.json",
}

BUILD_DIR = REPO_ROOT / "build"


def load_all(paths=None):
    """全ソースを読み、正規化済みレコードのリストを返す (横断リンク前)。

    plan はファイルが存在すれば読み、無ければスキップする。
    """
    paths = {**DEFAULT_PATHS, **(paths or {})}
    records = []
    records += load_aws(paths["aws"])
    records += load_azure(paths["azure"])
    records += load_google(paths["google"])
    plan_path = Path(paths["plan"]) if paths.get("plan") else None
    if plan_path and plan_path.exists():
        records += load_plan(plan_path)
    return records


def run_etl(paths=None, build_dir=BUILD_DIR, write_outputs=True):
    """正規化 + 横断リンクまで実行し (records, report) を返す。"""
    records = load_all(paths)
    upgraded = build_related(records)
    report = link_report(records)

    if write_outputs:
        build_dir = Path(build_dir)
        build_dir.mkdir(parents=True, exist_ok=True)
        (build_dir / "unified.json").write_text(
            json.dumps(records, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
        (build_dir / "link_report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
        (build_dir / "link_report.md").write_text(
            link_report_markdown(records), encoding="utf-8"
        )
        build_db(records, build_dir / "catalog.db")

    return records, report, upgraded


def main(argv=None):
    run_etl()
    report_path = BUILD_DIR / "link_report.md"
    print(report_path.read_text(encoding="utf-8"))
    print(f"wrote {BUILD_DIR}/unified.json, link_report.*, catalog.db")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
