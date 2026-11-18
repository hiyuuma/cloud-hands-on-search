# Run 2 報告 — T3 (検索) / T4 (推薦) / T5 (CLI)

状態: 完了 (2026-11-18)

## 実装したモジュール

標準ライブラリのみで実装 (テスト用 pytest のみ、Run 1 同様)。

| ファイル | 役割 |
|---|---|
| `db.py` (拡張) | `records_fts` FTS5 仮想テーブルを追加。`tokenize='trigram'` で title / title_ja / summary_ja / services (空白連結) / domain を索引化。`build_db` 時に自動投入。既存 records テーブルは非変更 |
| `search.py` (T3) | `search(db, query, limit=, cloud=, domain=, service=, level=, max_duration_min=, access=, priority=, plan_month=)`。FTS5 MATCH (全語 AND) + 絞り込みフィルタ。ランキングは「title/title_ja 全語一致 > bm25 > id」の完全決定的順序 |
| `recommend.py` (T4) | `recommend(records, minutes=, interests=, plan_month=)`。決定論的スコアリング + 空き時間内に収まる貪欲パック。`format_plan` で「今日の流れと所要時間・課金の見立て」テキストを生成 |
| `cli.py` (T5) | argparse CLI。`search / recommend / show / stats / export-plan`。build/catalog.db が無ければ自動で ETL 実行。`--db` でパス指定可 |
| `__init__.py` (修正) | etl の遅延 import に変更し `python -m hands_on_search.etl` の runpy RuntimeWarning を解消 (ついで対応) |

## 設計上の判断

- **trigram の選定**: unicode61 等は日本語を適切に分かち書きできず部分一致が
  効かないため、指示どおり trigram。FTS の MATCH 式は各トークンを `"` で
  囲み AND 結合 (特殊文字の注入を防止)。
- **3文字未満クエリ**: trigram は 3 グラム索引のため "AI" など 2 文字クエリは
  マッチしない。`LIKE %...%` 部分一致にフォールバック (検索対象列は同一)。
  また FTS が 0 件でも LIKE にフォールバックして救済。既知の制限として、
  LIKE フォールバックは単語中の部分文字列にもヒットする (例 "AI" が
  "Available" に一致)。
- **ランキング**: title/title_ja に全トークンがヒットしたレコードを最優先、
  次に bm25(records_fts) 昇順、最後に id 順。同じ入力で必ず同じ順序。
- **plan_month**: "2027-03 データ基盤 / 分析" のような月+テーマ複合値が
  あるため、フィルタもブーストも `startswith(月)` の前方一致。
- **推薦スコア**: タイトル/サービス一致 +3/語、要約一致 +2/語、計画月一致 +2、
  priority 高 +2 / 中 +1。関心キーワード指定時はキーワード非一致のレコードを
  除外。同点は所要時間昇順 → id で完全決定的。貪欲パックで duration_min
  判明分の合計が必ず空き時間以内。duration 不明は時間にカウントせず、
  判明分を詰めた後に末尾へ追加し「所要時間不明」と明示。
- **課金の見立て**: access 表記 (Subscription / Free / credits) をそのまま表示。
  空/unknown は「不明・要確認」。金額は推測しない旨を注記。

## ゴールデンクエリ実測 (plan フィクスチャ込み 896 件の DB)

- `Fargate` → 2 位に "Deploy and Scale Containerized Applications with AWS Fargate"
  (1 位は同名別ラボ "Create a CI/CD pipeline... AWS Fargate"、3 位は plan 側の
  同名レコード = T2 横断リンク先)。期待レコードは上位 5 件内 ✓
- `MCP` → 上位に "Develop a speech agent with the Azure Speech MCP server",
  "Integrate MCP Tools with Azure AI Agents", "Building Your First Model
  Context Protocol (MCP) Server" 等。タイトル/要約に MCP を含むレコードがヒット ✓
- `PostgreSQL` → 3 位に "Microsoft Applied Skills: Configure and migrate to
  Azure Database for PostgreSQL" ✓
- `Kubernetes` → "Deploy applications to Azure Kubernetes Service",
  "Kubernetes in Google Cloud" 等がヒット ✓

テスト: `tests/test_search.py::test_golden_*` で機械検証済み。

## CLI 動作確認 (実測)

    PYTHONPATH=src .venv/bin/python -m hands_on_search.cli search Fargate --limit 3
    → 2 件ヒット、両方 link=direct の URL 付きで表示

    ... recommend --minutes 90 --interest MCP コンテナ
    → 「今日の流れ」形式で 51分+30分+不明時間の候補、理由・課金の見立て付き

    ... stats → aws:167 / azure:550 / google:176、direct 727 (81.4%)

    ... export-plan --interest MCP --out plan.md
    → Markdown に [タイトル](URL) リンクで書き出し

    ... show plan:HO-SAMPLE-003 (plan フィクスチャ込み DB で確認済み)

## テスト結果

実行コマンド:

    .venv/bin/python -m pytest tests/ -q

結果: **42 passed** (0.67s) — Run 1 の 16 テスト + 新規 26 テスト

- `test_search.py` (10): ゴールデンクエリ 4 件、タイトル>要約ランキング、
  決定性、各フィルタ、link 付与、短クエリ LIKE フォールバック、未知フィルタ拒否
- `test_recommend.py` (9): 決定性、時間上限遵守、理由の付与、関心マッチ、
  plan_month ブースト、同伴型テキスト、access 不明表記、空結果
- `test_cli.py` (7): search/recommend/show/stats/export-plan の出力、
  URL 導線表示、not found

## 既知の制限

- LIKE フォールバック (3文字未満クエリ or FTS 0件) は単語中の部分一致にも
  ヒットするためノイズが出得る ("AI" → "Available" 等)。
- FTS5 MATCH は全語 AND。OR 検索・フレーズ検索・除外語は未対応。
- 推薦の貪欲パックは最適組合せ (ナップサック) ではなくスコア順の近似。
  duration 不明レコードは枠を消費しないため、実際には時間超過し得る旨を
  出力に注記している。
- CLI 実行には `PYTHONPATH=src` が必要 (パッケージ未インストールのため)。
  README に明記。
- Run 1 同様、`data/local/plan.json` が無い環境では plan カタログは 0 件。
  stats・検索はそのまま動作する。
