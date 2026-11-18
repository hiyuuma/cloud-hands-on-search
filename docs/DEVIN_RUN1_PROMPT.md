# DEVIN RUN 1 指示書 — T1 (正規化ETL + URL導線) と T2 (横断リンク)

あなたは Devin CLI (SWE-2) として、このワークスペースで作業する自律実装担当です。
計画の正本は docs/PLAN.md です。まずそれを全文読んでください。

## 今回の範囲 (Run 1)

T1 と T2 のみを実装してください。T3 以降 (検索・推薦・CLI) は次回ランで行うので、
今回は検索 UI や CLI を作らないでください。ただし T3 が使いやすい形で
モジュール境界を設計してください。

## 成果物

1. `src/hands_on_search/__init__.py` と ETL モジュール群
   - 4つの入力形式を読むローダ:
     - data/vendor/aws_builder_labs.json (JSON 配列, 167件)
     - data/vendor/azure_learn.json (dict の items キー, 550件)
     - data/vendor/google_skills.json (JSON 配列, 176件)
     - 計画オーバーレイ: data/local/plan.json が存在すれば読む (無ければスキップ)。
       テストでは tests/fixtures/plan_sample.json (合成3件) を使う
   - docs/PLAN.md の統一スキーマへの正規化 (duration は分に変換、不明は null。
     推測で埋めない。元のレコードは raw に保持)
   - URL導線 (PLAN の「URL導線仕様」が必須要件):
     - link = {url, kind: direct|search, source}
     - direct は元データに実在する URL のみ。捏造禁止
     - Azure は url_ja を主導線にする
     - AWS で直接URLが無い件は公式検索パターン
       https://skillbuilder.aws/search?searchText=<URLエンコードしたタイトル>&typeId=aws_builder_lab
       で kind=search の導線を生成する
     - Google / plan で直接URLが無い件は、確実な公式検索パターンが無いので
       kind=search の生成はせず link.url を空、kind を "none" とし、
       link_report で件数が分かるようにする (捏造しない)
   - 統一データの書き出し: build/unified.json (生成物) と、
     SQLite DB を作るためのデータ層 (DB ファイル自体は git 対象外)
   - link_report: カタログ別に direct/search/none の件数を数える関数と
     レポート出力 (Markdown か JSON)
2. T2 横断リンク:
   - タイトル正規化 (小文字化、記号・空白の統一、日英の表記ゆれは分かる範囲) と
     URL 一致で、異なるカタログ間の同一ラボ候補を related として記録する
   - 削除・マージはしない。related は相互参照の ID リストとする
   - related 先に direct URL があり自レコードに無い場合、link を direct に格上げし
     source に引き継ぎ元カタログを記録する
3. pytest テスト一式 (tests/):
   - vendor 893件 (167+550+176) が1件も落ちずに取り込める
   - plan フィクスチャ3件が取り込める
   - 全レコードに link フィールドがあり、direct の URL は元データの URL 集合に
     必ず含まれる (捏造検出)
   - AWS の search 導線が上記パターンどおりに生成される
   - Azure の主導線が url_ja である
   - フィクスチャ HO-SAMPLE-003 (Fargate) が AWS カタログの
     "Deploy and Scale Containerized Applications with AWS Fargate" と
     related で結ばれる
   - duration 正規化の代表例 (例: "1h" -> 60, "1h 30m" -> 90, 空欄 -> null)
4. `reports/devin-run1/REPORT.md`: 完了報告。実装したモジュール一覧、テスト結果
   (実行コマンドと件数)、link カバレッジの実数、未達や判断に迷った点を正直に書く。
   進捗はこのファイルを逐次更新し、途中で終わっても完了分が残るようにすること

## 制約

- Python 3.12 標準ライブラリのみ (テスト用 pytest は可)。pip 追加禁止
- 元データファイル (data/vendor/*.json) は変更しない
- git コミットはしない (司令塔が検収してからコミットする)
- テストは `python3 -m pytest tests/ -q` で実行できる形にする
- 日本語の要約文など成果物に日本語の読み物を含める場合は、読みやすく推敲すること

## 完了の定義

上記テストが全て通り、REPORT.md に実数が記録されていること。
