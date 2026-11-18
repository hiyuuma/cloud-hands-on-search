# DEVIN RUN 5 指示書 — 第2波24カタログの統合

あなたは Devin CLI (SWE-2) として、このワークスペースで作業する自律実装担当です。
計画の正本は docs/PLAN.md、Run 1〜4 の報告 (reports/devin-run1〜4/REPORT.md) と
第2波の収集報告 (reports/catalog-expansion/*.md) をまず読んでください。
既存の検収済みモジュールとテスト (84件) を壊さないことが前提です。
Run 4 の統合パターン (ローダ追加・duration 変換・導線テスト拡張・ETL 再生成・
README 更新) をそのまま踏襲してください。

## 対象データ (data/vendor-staging/ に検証済みで格納済み、全24ファイル・491件)

| ファイル | 件数 | source_catalog キー |
|---|---|---|
| alibaba_academy.json | 13 | alibaba |
| anthropic_academy.json | 29 | anthropic |
| cisco_u.json | 23 | cisco |
| confluent.json | 27 | confluent |
| databricks_academy.json | 51 | databricks |
| datadog.json | 25 | datadog |
| elastic.json | 7 | elastic |
| fortinet.json | 13 | fortinet |
| freecodecamp.json | 12 | freecodecamp |
| huggingface_learn.json | 12 | huggingface |
| ibm_skillsbuild.json | 4 | ibm |
| kaggle_learn.json | 17 | kaggle |
| langchain_academy.json | 18 | langchain |
| mongodb_university.json | 21 | mongodb |
| neo4j_graphacademy.json | 60 | neo4j |
| nextjs_learn.json | 31 | nextjs |
| nvidia_dli.json | 11 | nvidia |
| portswigger.json | 31 | portswigger |
| redhat_developer.json | 12 | redhat |
| redis_university.json | 4 | redis |
| salesforce_trailhead.json | 22 | salesforce |
| sap_learning.json | 17 | sap |
| servicenow.json | 20 | servicenow |
| snowflake.json | 11 | snowflake |

いずれも全レコードに実在確認済みの直接 URL があり、title / url / type / level /
duration_text / description / domain / services / priority_for_user / summary_ja
を持つ。フィールドの欠けは空文字または null で来る。
KubeAcademy は公式終了済みのためユーザーの決定で除外済み (staging に無いのが正)。

## 実装内容

1. staging の24ファイルを data/vendor/ へ移し、各カタログのローダを追加して
   ETL に組み込む。ID は既存規則に倣いカタログ接頭辞つきで一意にする
2. 統一スキーマへのマッピング:
   - duration_text の新しい表記 ("14 hours" / "18 hours" / "45m" / "55m" /
     "1h" / 推奨ペース表記など) を可能な範囲で duration_min に変換する。
     変換できない表記は None にし、カタログ別の件数を REPORT に書く
   - level は既存の正規化規則に合わせる (出典に無いものは空のまま推測しない)
   - billing: 原則として全件「無料」(収集段階で無料確認済みのものだけを
     収録している)。例外を正直に扱うこと:
     - anthropic: サイトに料金表示自体が無く「無料」と断定できない。
       billing は無料にせず、既存の「不明・要確認」に相当する扱いにし、
       根拠 (開始ボタンに課金表示なし) を REPORT に書く
     - redhat: 教材は無料だが一部は実習に無償トライアル登録が必要。
       billing は無料のままでよいが、その旨を REPORT に明記する
     - elastic: 3件は無料確認度が一段低い (収集報告参照)。統合はするが
       REPORT にその旨を明記する
   - priority_for_user / summary_ja / domain / services は staging の値を尊重する
3. 導線: staging の URL は全件 kind=direct (実在確認済み)。「direct は元データに
   実在するものだけ」という機械テストの対象範囲を新しい元データにも広げる
4. 横断リンク (T2) の対象に新カタログも含める (既存ルールのまま。無理に増やさない)
5. テスト追加: カタログ別ローダ、duration 変換、総件数 (2,073件になるはず:
   既存1,582 + 新規491)、ゴールデンクエリの追加検証 (例: LangGraph で
   LangChain Academy がヒットする、SQLインジェクションで PortSwigger が
   ヒットする、Kubernetes で Red Hat のパスがヒットする、FortiAuthenticator で
   Fortinet がヒットする、Next.js で Next.js Learn がヒットする)
6. ETL 再生成: build/unified.json、link_report、catalog.db を更新し、
   web/unified-compact.json も再生成する
7. README のカタログ一覧と件数を更新する

## 成果物

- 上記の実装とテスト (既存84件 + 新規が全て通ること)
- `reports/devin-run5/REPORT.md`: カタログ別の統合件数と充足率
  (duration/level/billing)、duration 変換できなかった件数と理由、導線内訳、
  ゴールデンクエリ実測、billing 判断の根拠 (特に anthropic の扱い)、
  既知の制限を正直に書く。進捗は逐次更新すること

## 制約

- Python 3.12 標準ライブラリのみ (テスト用 pytest は可)。pip 追加禁止
- 元データの内容 (タイトル・URL) は改変しない (配置移動と形式変換のみ)
- git コミットはしない (司令塔が検収してからコミットする)
- テストは `.venv/bin/python -m pytest tests/ -q` で実行できる形にする
