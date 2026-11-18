# Kaggle Learn カタログ収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/kaggle_learn.json` (**17件**)

## 使った公式ページ

| ページ | URL | 用途 |
|---|---|---|
| Kaggle Learn トップ (Courses 一覧) | https://www.kaggle.com/learn | 全マイクロコースの列挙 (タイトル・説明・各コースへのリンク) の母集団 |
| 各コースページ (15件分) | https://www.kaggle.com/learn/<slug> | 所要時間 "Hours to earn certificate" の原文確認 |

## 件数と充足率

- 収録件数: **17件** (全て type=course)
- duration_text 充足: 15/17件 — 各コースページの "Hours to earn certificate: N (estimated)" を原文形式で転記
- level 充足: 0/17件 — 公式ページにレベル表記がないため空欄 (推測で埋めていない)
- description: 全件に /learn 一覧ページの公式1行説明を設定

## カバレッジの限界

- /learn ページの "Courses" セクションに掲載された17コースが現在の全マイクロコースであり、全件収録した。
- 同ページの "Guides" (5-Day AI Agents Intensive 等の学習ガイド集) はコースではないため対象外とした。
- **Intermediate Machine Learning と Geospatial Analysis の2件**は、個別コースページ取得時に Kaggle 側APIのレート制限 (429) でページが描画エラーとなり、所要時間を確認できなかった。存在・タイトル・説明は公式 /learn 一覧で確認済みのため収録し、duration_text は空欄とした。
- 過去に存在した "Intro to LLMs" は現在の公式 /learn 一覧に掲載がなく、収録していない。

## 検証方法

1. 公式 /learn ページの Courses 一覧から17コースを列挙し、リンクURLをそのまま転記 (組み立て・推測なし)
2. 各コースページを実際に開き、ページタイトルと所要時間表示を確認 (15件成功、2件は上記のとおり描画エラー)
3. 全コースともコースページに "No cost, like all Kaggle Learn Courses" と明記されており、無料であることを確認
