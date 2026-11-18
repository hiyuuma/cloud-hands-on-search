# Databricks Academy カタログ収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/databricks_academy.json` (**51件**)

## 使った公式ページ

| ページ | URL | 用途 |
|---|---|---|
| Databricks Academy 公開コースAPI (Docebo LMS) | https://customer-academy.databricks.com/learn/v1/courses (全10ページ) | カタログ全件 (総数999件) の列挙。タイトル・コースID・スラッグ・種別・価格・所要秒数を一次データとして取得 |
| Databricks 公式GitHub (databricks-solutions/databricks-quest 設計ドキュメント) | GitHub 上の同リポジトリ | コースURLの正規形式 `https://customer-academy.databricks.com/learn/courses/{id_course}/{slug_name}` が公式に検証済み (200応答・ログイン不要で到達) であることの根拠 |

## 件数と充足率

- 収録件数: **51件** (全て type=course、英語版の無料セルフペースコース)
- duration_text 充足: 51/51件 — API の所要秒数を時間表記に変換して転記 (例: 7200秒→"2 hours")
- level 充足: 0/51件 — API にレベル項目がないため空欄 (推測で埋めていない)
- description 充足: 25/51件 — API の公式説明文を確認できたもののみ転記し、残りは空欄

## 無料/有料の切り分け方法

- API の `course_type` が `elearning` (セルフペース) かつ `price` が `"0"` のものだけを収録した。
- 講師主導トレーニング (ILT、`course_type` = `classroom`) は収録対象外。API 全999件の過半を占めるが、無料セッション混在のため正確な件数は未集計 (件数のみの報告が求められる場合も、推測値は記載しない)。
- 同名コースには有料版が併存する (例: カスタマー向け有料版 $75、ブレンデッドラーニング $500) ため、タイトルではなく価格フィールドで厳密に切り分けた。収録したのは無料版 (価格 $0) のIDのみ。

## カバレッジの限界

- **英語オリジナルのみ収録**。同一コースのローカライズ版 (日本語・韓国語・フランス語・スペイン語・ポルトガル語・中国語) は重複として除外した (日本語版も多数存在する)。
- Learning Plan (学習パス) は `/courses` API の対象外のため未収録。パス単位の導線が必要なら別途収集が要る。
- コース内の Knowledge Check 単体クイズ (コースの付属物) は除外した。ただし認定アセスメント自体 (Fundamentals Accreditation 等) は独立コースとして収録した。
- コースページはログイン/JS描画が前提の LMS ページで、テキスト取得では内容を抽出できなかった (HTTP 200 の到達は確認)。そのため URL の実在は「API が返す実在の id_course と slug_name の組み合わせ」+「公式ドキュメント記載のURL形式」で担保しており、推測で組み立てた URL は1件もない。

## 検証方法

1. 公式APIの全10ページ (999件) を走査し、`elearning` かつ `price="0"` かつ英語のものを抽出
2. 各レコードの id_course と slug_name は API レスポンスの原文をそのまま使用 (URL の推測・組み立てなし)
3. 出力JSONで URL の一意性と必須フィールド (title/url/type/summary_ja) の充足を機械検証済み
