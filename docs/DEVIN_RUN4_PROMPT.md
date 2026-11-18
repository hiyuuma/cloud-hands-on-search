# DEVIN RUN 4 指示書 — 新規4カタログの統合

あなたは Devin CLI (SWE-2) として、このワークスペースで作業する自律実装担当です。
計画の正本は docs/PLAN.md、Run 1〜3 の報告 (reports/devin-run1〜3/REPORT.md) と
収集報告 (reports/catalog-expansion/*.md) をまず読んでください。
既存の検収済みモジュールとテスト (73件) を壊さないことが前提です。

## 対象データ (data/vendor-staging/ に検証済みで格納済み)

| ファイル | 件数 | source_catalog キー |
|---|---|---|
| hashicorp.json | 499 | hashicorp |
| linux_foundation.json | 59 | linux_foundation |
| github_skills.json | 42 | github_skills |
| oracle_oci.json | 89 | oracle |

いずれも全レコードに実在確認済みの直接 URL があり、title / url / type / level /
duration_text / description / domain / services / priority_for_user / summary_ja
を持つ (linux_foundation は price_text も持つ)。フィールドの欠けは空文字で来る。

## 実装内容

1. staging の4ファイルを data/vendor/ へ移し、各カタログのローダを追加して
   ETL に組み込む。ID は既存規則に倣いカタログ接頭辞つきで一意にする
2. 統一スキーマへのマッピング:
   - duration_text の多様な表記 ("26h 30m" / "1 hour, 30 minutes" /
     "2 hours, 15 minutes" / "45 minutes" / "15 minutes" / "3 hours") を
     duration_min に変換する。変換できない表記は None にし、件数を REPORT に書く
   - level は既存の正規化規則に合わせる (出典に無いものは空のまま推測しない)
   - billing: 出典に基づく判断を REPORT に明記したうえで設定する。
     目安 — GitHub Skills / HashiCorp チュートリアル / Oracle MyLearn・LiveLabs は
     無料。Linux Foundation は price_text があるものは有料 (価格原文は raw に残す)、
     "Free" 表記は無料、価格不明は「不明・要確認」
   - priority_for_user / summary_ja / domain / services は staging の値を尊重する
3. 導線: staging の URL は全件 kind=direct (実在確認済み)。既存の
   「direct は元データに実在するものだけ」という機械テストが staging 由来にも
   効くよう、テストの対象範囲を新しい元データにも広げる
4. 横断リンク (T2) の対象に新カタログも含める (既存ルールのまま。無理に
   増やさない)
5. テスト追加: カタログ別ローダ、duration 変換、総件数 (1,582件になるはず:
   既存893 + 新規689)、ゴールデンクエリの追加検証 (例: Terraform で
   HashiCorp 公式チュートリアルが上位に来る、Kubernetes で Linux Foundation の
   コースがヒットする、MCP で LiveLabs の "Put AI Agents to Work with MCP" が
   ヒットする)
6. ETL 再生成: build/unified.json、link_report、catalog.db を更新し、
   web/unified-compact.json も再生成する
7. README のカタログ一覧と件数を更新する

## 成果物

- 上記の実装とテスト (既存73件 + 新規が全て通ること)
- `reports/devin-run4/REPORT.md`: カタログ別の統合件数と充足率
  (duration/level/billing)、duration 変換できなかった件数と理由、導線内訳、
  ゴールデンクエリ実測、billing 判断の根拠、既知の制限を正直に書く。
  進捗は逐次更新すること

## 制約

- Python 3.12 標準ライブラリのみ (テスト用 pytest は可)。pip 追加禁止
- 元データの内容 (タイトル・URL) は改変しない (配置移動と形式変換のみ)
- git コミットはしない (司令塔が検収してからコミットする)
- テストは `.venv/bin/python -m pytest tests/ -q` で実行できる形にする
