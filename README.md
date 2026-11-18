# cloud-hands-on-search

3クラウド (AWS / Azure / Google) + HashiCorp / Linux Foundation / GitHub Skills /
Oracle (OCI) の学習カタログを統合し、日本語で検索・推薦でき、
見つけたらその場で始められる URL 導線が必ず付く検索エンジン。

開発中です。計画と進捗は docs/PLAN.md と docs/LEDGER.md を参照してください。

## データについて

- data/vendor/ の各社カタログは、公式カタログの公開情報をもとに作成した
  メタデータです (計 1,582 件):

  | カタログ | ファイル | 件数 |
  |---|---|---|
  | AWS Skill Builder (Builder Labs) | aws_builder_labs.json | 167 |
  | Microsoft Learn (Azure) | azure_learn.json | 550 |
  | Google Skills | google_skills.json | 176 |
  | HashiCorp Developer チュートリアル | hashicorp.json | 499 |
  | Linux Foundation トレーニング | linux_foundation.json | 59 |
  | GitHub Skills | github_skills.json | 42 |
  | Oracle MyLearn / LiveLabs (OCI) | oracle_oci.json | 89 |

- 個人の学習計画はこのリポジトリに含みません。手元の計画ファイルは
  data/local/plan.json に置くとローカルオーバーレイとして取り込まれます
  (data/local/ は .gitignore 対象です)

## URL導線について

全レコードに link が付きます。kind=direct はラボへの直行URL (元データに実在する
もののみ)、kind=search は公式検索への導線です。直接URLを推測で作ることはしません。

## 使い方 (CLI)

事前に ETL で DB を生成します (build/ は生成物です):

    PYTHONPATH=src python3 -m hands_on_search.etl

CLI は argparse ベースです。build/catalog.db が無い場合は自動で ETL を実行します。

    # キーワード検索 (絞り込み: --cloud/--domain/--service/--level/
    #   --max-minutes/--access/--priority/--month, --limit で件数)
    # --mode and(既定)/or/phrase で検索モードを切替
    PYTHONPATH=src python3 -m hands_on_search.cli search Fargate --limit 5
    PYTHONPATH=src python3 -m hands_on_search.cli search PostgreSQL --cloud Azure --max-minutes 120
    PYTHONPATH=src python3 -m hands_on_search.cli search "Fargate PostgreSQL" --mode or
    PYTHONPATH=src python3 -m hands_on_search.cli search "Kubernetes in Google Cloud" --mode phrase

    # 空き時間と関心キーワードから推薦 (所要時間と課金の見立て付き)
    PYTHONPATH=src python3 -m hands_on_search.cli recommend --minutes 90 --interest MCP コンテナ --month 2026-11

    # レコード詳細
    PYTHONPATH=src python3 -m hands_on_search.cli show aws:deploy-and-scale-containerized-applications-with-aws-fargate

    # カタログ別件数と link カバレッジ
    PYTHONPATH=src python3 -m hands_on_search.cli stats

    # 推薦結果を Markdown に書き出し (タイトルはリンク)
    PYTHONPATH=src python3 -m hands_on_search.cli export-plan --minutes 90 --interest MCP --out plan.md

検索は SQLite FTS5 (trigram) で title / title_ja / summary_ja / services /
domain を対象にします。タイトル一致が要約一致より上位になり、同じ入力では
常に同じ順序です。検索・推薦のすべての出力に link (URL 導線) が付きます。

テスト:

    .venv/bin/python -m pytest tests/ -q
