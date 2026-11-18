# freeCodeCamp カタログ収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/freecodecamp.json` (**12件**)

## 使った公式ページ

| ページ | URL | 用途 |
|---|---|---|
| freeCodeCamp カリキュラム トップ | https://www.freecodecamp.org/learn | 認定 (certification) の列挙の母集団 |
| 各認定ページ (12件分) | https://www.freecodecamp.org/learn/<slug>/ | タイトル・公式説明文の確認 |
| freeCodeCamp 公式FAQ (About) | https://opensource.freecodecamp.org/about/ | "Each certification takes around 300 hours" の出典 |
| 公式フォーラム発表 (Major Curriculum Update) | https://forum.freecodecamp.org/t/major-curriculum-update-introducing-new-freecodecamp-certifications/762070 | 中間6認定が各約300時間、Full-Stack 総計約1,800時間の出典 |

## 件数と充足率

- 収録件数: **12件** (全て type=certification)
  - コア認定 7件 (Responsive Web Design / JavaScript / Front-End Development Libraries / Python / Relational Databases / Back-End Development and APIs / Certified Full-Stack Developer Curriculum)
  - プロフェッショナル認定 1件 (Free Foundational C# with Microsoft)
  - 言語認定 (Beta) 4件 (A2 English / B1 English / A1 Spanish / A1 Chinese)
- duration_text 充足: 7/12件 — コア6認定は公式FAQの "around 300 hours"、Full-Stack は公式発表の総計約1,800時間を転記。C# 認定と言語認定は公式の時間表記がなく空欄
- level 充足: 4/12件 — 言語認定のみ CEFR レベル (タイトル内表記) を設定。開発系認定は公式ページにレベル表記がなく空欄
- description: 全件に各認定ページの公式説明文を設定

## カバレッジの限界

- 現在の /learn ページに掲載された認定は全件収録した。
- /learn 内の "The Odin Project - freeCodeCamp Remix" "Coding Interview Prep" "Project Euler" "Rosetta Code" は認定ではないため対象外とした。
- 旧カリキュラムの認定 (Data Visualization、Scientific Computing with Python、Data Analysis with Python、Information Security、Machine Learning with Python、College Algebra with Python、Legacy Full Stack 等) はアーカイブページ側に移行しており、現行 /learn の掲載分のみを対象としたため未収録。
- 言語認定4件は Beta 表記で、うち Spanish / Chinese は認定試験が未公開 (開発中) と公式ページに明記されている。

## 検証方法

1. 公式 /learn ページから認定を列挙し、リンクURLをそのまま転記 (組み立て・推測なし)
2. 12件すべての認定ページを実際に開き、タイトルと説明文の対応を確認
3. 所要時間は公式FAQと公式フォーラム発表の表記に基づく (個別認定ページには時間表記なし)
