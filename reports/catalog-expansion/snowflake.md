# Snowflake (Snowflake University) カタログ収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/snowflake.json` (**11件**)

## 使った公式ページ

| ページ | URL | 用途 |
|---|---|---|
| Hands-On Essentials トラックページ | https://learn.snowflake.com/en/pages/hands-on-essentials-track/ | 「The courses in this track are free」と無料が公式明記。バッジワークショップ6件の列挙 |
| 各ワークショップページ (6件) | https://learn.snowflake.com/en/courses/uni-essdww101/ 等 | 所要時間 "Most learners take between 8 and 12 hours" の原文確認 |
| learn.snowflake.com ホームページ | https://learn.snowflake.com/ | Level Up シリーズが「online for free」と公式明記されていることの確認 |
| Level Up 個別コースページ (2件を実地確認) | https://learn.snowflake.com/en/courses/OD-LVLUP-104/ 、 https://learn.snowflake.com/en/courses/OD-LVLUP-301/ | 本番ドメインでの実在とシリーズ構成の確認 |
| MFA コースページ | https://learn.snowflake.com/en/courses/OD-MFA/ | 本番ドメインでの実在確認。無料であることは公式データシート等の「free on-demand course」明記で確認 |

## 件数と充足率

- 収録件数: **11件** (lab 6件 / course 5件)
- duration_text 充足: 6/11件 — ワークショップ各ページの所要時間原文を転記。Level Up と MFA は個別の所要時間表記を確認できず空欄
- level 充足: 0/11件 — 公式ページにレベル表記がないため空欄 (推測で埋めていない)
- description 充足: 1/11件 — MFA のみ公式 Overview を転記

## 無料/有料の切り分け方法

- 公式ページに**無料であることが明言されたものだけ**を収録した (Hands-On Essentials トラックの無料明記、Level Up の無料明記、MFA の free on-demand 明記)。
- SnowPro Core Certification Prep Course は有料のため除外 (認定対策コース)。
- 講師主導トレーニング (ILT) は収録対象外。例: Data Science Training (3日)、Snowflake Data Engineer Training (3日)、Snowflake GenAI Training (2日)。なお第三者の集約サイトには総数816件という数字があるが、非公式のため公式件数としては採用しない。

## カバレッジの限界

- 以下のオンデマンドコースは存在を確認したが、**無料であることの公式明記を確認できなかったため未収録** (無料の可能性はあるが、確認できないものを無料として収録しない方針):
  - Snowflake Practitioner Training (OD-SPP)
  - CoCo Essentials (OD-COCOESS)
  - Getting Started with CoCo Desktop (OD-COCODSK)
  - Snowflake Platform On-Demand Training
- Snowflake Multi-Factor Authentication Essentials (MFA) は、当初サンドボックス側ドメインでしか確認できなかったが、本番 learn.snowflake.com のコースページを実地で開き実在を確認したため収録した。
- Level Up シリーズは全モジュール (First Concepts 9モジュール等) を網羅していない。コースコードとタイトルを公式に確認できた4モジュールのみ収録した。

## 検証方法

1. 公式トラックページ・ホームページの無料明記を根拠に母集団を確定
2. ワークショップ6件はトラックページ掲載のリンクをそのまま転記 (組み立て・推測なし)
3. Level Up 2件 (OD-LVLUP-104 / OD-LVLUP-301) と MFA (OD-MFA) は本番ページを実際に開いてタイトルと実在を確認。残りの Level Up 2件 (OD-LVLUP-202 / OD-LVLUP-308) は公式検索結果で本番ドメインのURLとタイトルを確認
4. 出力JSONで URL の一意性と必須フィールドの充足を機械検証済み
