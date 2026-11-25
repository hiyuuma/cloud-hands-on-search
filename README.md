# cloud-hands-on-search

3クラウド (AWS / Azure / Google) + HashiCorp / Linux Foundation / GitHub Skills /
Oracle (OCI) + 各社公式ラーニングカタログ (計38ソース) を統合し、
日本語で検索・推薦でき、
見つけたらその場で始められる URL 導線が必ず付く検索エンジン。

開発中です。計画と進捗は docs/PLAN.md と docs/LEDGER.md を参照してください。

## データについて

- data/vendor/ の各社カタログは、公式カタログの公開情報をもとに作成した
  メタデータです (計 2,243 件):

  | カタログ | ファイル | 件数 |
  |---|---|---|
  | AWS Skill Builder (Builder Labs) | aws_builder_labs.json | 167 |
  | Microsoft Learn (Azure) | azure_learn.json | 550 |
  | Google Skills | google_skills.json | 176 |
  | HashiCorp Developer チュートリアル | hashicorp.json | 499 |
  | Linux Foundation トレーニング | linux_foundation.json | 59 |
  | GitHub Skills | github_skills.json | 42 |
  | Oracle MyLearn / LiveLabs (OCI) | oracle_oci.json | 89 |
  | Alibaba Cloud Academy | alibaba_academy.json | 13 |
  | Anthropic Academy | anthropic_academy.json | 29 |
  | Cisco U. | cisco_u.json | 23 |
  | Confluent Developer | confluent.json | 27 |
  | Databricks Academy | databricks_academy.json | 51 |
  | Datadog Learning Center | datadog.json | 25 |
  | Elastic Training | elastic.json | 7 |
  | Fortinet Training Institute | fortinet.json | 13 |
  | freeCodeCamp | freecodecamp.json | 12 |
  | Hugging Face Learn | huggingface_learn.json | 13 |
  | IBM SkillsBuild | ibm_skillsbuild.json | 4 |
  | Kaggle Learn | kaggle_learn.json | 18 |
  | LangChain Academy | langchain_academy.json | 18 |
  | MongoDB University | mongodb_university.json | 21 |
  | Neo4j GraphAcademy | neo4j_graphacademy.json | 60 |
  | Next.js Learn | nextjs_learn.json | 31 |
  | NVIDIA Deep Learning Institute | nvidia_dli.json | 11 |
  | PortSwigger Web Security Academy | portswigger.json | 31 |
  | Red Hat Developer | redhat_developer.json | 12 |
  | Redis University | redis_university.json | 4 |
  | Salesforce Trailhead | salesforce_trailhead.json | 22 |
  | SAP Learning | sap_learning.json | 17 |
  | ServiceNow | servicenow.json | 20 |
  | Snowflake | snowflake.json | 11 |
  | Cloudflare Developers (Agents/MCP) | cloudflare_agents.json | 11 |
  | Cohere LLM University | cohere_llmu.json | 10 |
  | DeepLearning.AI | deeplearning_ai.json | 45 |
  | Microsoft 公式カリキュラム (GitHub) | microsoft_curricula.json | 52 |
  | OpenAI Academy | openai_academy.json | 14 |
  | Palantir Learn | palantir_learn.json | 26 |
  | Vercel Academy | vercel_academy.json | 10 |

- 個人の学習計画はこのリポジトリに含みません。手元の計画ファイルは
  data/local/plan.json に置くとローカルオーバーレイとして取り込まれます
  (data/local/ は .gitignore 対象です)

## URL導線について

全レコードに link が付きます。kind=direct はラボへの直行URL (元データに実在する
もののみ)、kind=search は公式検索への導線です。直接URLを推測で作ることはしません。

各レコードの link_lang は「収録されているリンク URL が指すページの言語」
("ja" / "en") です。URL に日本語ロケールが明示されているもの
(learn.microsoft.com/ja-jp/、academy.claude.com/ja/、skills.google の
locale=ja、oracle.com の japanese- スラグ) のみ "ja" と判定し、それ以外は
"en" です。プラットフォームに日本語版が別途存在しても、収録リンクが
英語ページなら "en" になります (リンク先の言語が定義であり、日本語版の
有無とは別です)。現状の内訳は ja 660件 / en 1,583件です。

## 使い方 (CLI)

事前に ETL で DB を生成します (build/ は生成物です):

    PYTHONPATH=src python3 -m hands_on_search.etl

CLI は argparse ベースです。build/catalog.db が無い場合は自動で ETL を実行します。

    # キーワード検索 (絞り込み: --cloud/--domain/--service/--level/
    #   --max-minutes/--access/--priority/--month/--lang, --limit で件数)
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
