# DEVIN RUN 2 指示書 — T3 (検索) / T4 (推薦) / T5 (CLI)

あなたは Devin CLI (SWE-2) として、このワークスペースで作業する自律実装担当です。
計画の正本は docs/PLAN.md、Run 1 の成果と報告は reports/devin-run1/REPORT.md です。
まず両方を読んでください。Run 1 のモジュール (loaders / normalize / related /
link_report / db / etl) は検収済みなので、壊さないでください。

## 今回の範囲 (Run 2)

T3・T4・T5 を実装してください。

### T3 検索

- SQLite FTS5 (tokenize='trigram') の仮想テーブルで title / title_ja /
  summary_ja / services / domain を全文検索する (db.py の土台を拡張してよい)
- 検索 API: キーワード + 絞り込み (cloud / domain / service / level /
  duration_min 上限 / access / priority / plan_month)
- ランキング: タイトル一致を要約一致より重くする。決定的 (同じ入力で同じ順序)
- ゴールデンクエリのテスト (期待レコードが上位5件以内):
  - "Fargate" → "Deploy and Scale Containerized Applications with AWS Fargate"
  - "MCP" → タイトルか要約に MCP を含むレコードがヒットする
  - "PostgreSQL" → Azure の "Configure and migrate to Azure Database for PostgreSQL"
  - "Kubernetes" → Kubernetes を含むレコードがヒットする

### T4 推薦

- 入力: 空き時間 (分)、関心キーワード (複数可)、計画月 (例 "2026-11")
- 出力: 候補リスト (合計所要時間が空き時間を超えない組み合わせを優先) と
  同伴型フォーマット「今日の流れと所要時間・課金の見立て」テキスト
  - 課金の見立ては access の表記 (Subscription / Free / credits) に基づき、
    不明なものは「不明・要確認」と正直に書く。推測で金額を書かない
- スコアリングは決定論的にし、内訳 (なぜ選ばれたか) を各候補に付ける
- テスト: 同じ入力で同じ結果、時間上限を守る、理由が付く

### T5 CLI

- `python3 -m hands_on_search.cli` で動く argparse ベースの CLI
  - search <query> [--cloud AWS] [--max-minutes 60] [--limit 10]
  - recommend [--minutes 90] [--interest MCP コンテナ] [--month 2026-11]
  - show <id>
  - stats (カタログ別件数と link カバレッジ)
  - export-plan [--minutes 90] [--interest ...] [--out plan.md]
    (推薦結果を Markdown で書き出し、全タイトルを URL 導線リンクにする)
- 検索・推薦の全出力に必ず link を表示する (URL 導線仕様)
- README.md に使い方の節を追記する

## 成果物

1. 上記を実装するモジュール (検索は search.py、推薦は recommend.py、
   CLI は cli.py を想定。既存構成に合わせた変更は可)
2. pytest テスト追加 (tests/)。Run 1 の既存16テストも含め全て通ること
3. `reports/devin-run2/REPORT.md`: 完了報告。実装モジュール、テスト結果
   (実行コマンドと件数)、ゴールデンクエリの実測結果、判断した点と既知の制限を
   正直に書く。進捗は逐次更新し、途中で終わっても完了分が残るようにする
4. ついでに Run 1 で報告された `python -m hands_on_search.etl` の
   RuntimeWarning が簡単に直せる場合は直してよい (必須ではない)

## 制約

- Python 3.12 標準ライブラリのみ (テスト用 pytest は可)。pip 追加禁止
- 元データファイル (data/vendor/*.json) は変更しない
- git コミットはしない (司令塔が検収してからコミットする)
- テストは `.venv/bin/python -m pytest tests/ -q` で実行できる形にする
