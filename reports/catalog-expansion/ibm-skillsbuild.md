# IBM SkillsBuild カタログ収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/ibm_skillsbuild.json` (**4件**)

## 使った公式ページ

| ページ | URL | 用途 |
|---|---|---|
| IBM SkillsBuild Learning Catalog | https://skillsbuild.org/learning-catalog | カタログ本体 (ただし後述のとおり中身は取得不可) |
| Credly IBM SkillsBuild 組織ページ | https://www.credly.com/org/ibm-skillsbuild | 発行元の確認 |
| Credly バッジページ (4件分) | https://www.credly.com/org/ibm-skillsbuild/badge/<slug> | 各認定パス (デジタルクレデンシャル) のタイトル・説明・レベル・無料可否の確認 |

## 件数と充足率

- 収録件数: **4件** (全て type=learning-path、デジタルクレデンシャル付きの学習パス)
  - Cybersecurity Fundamentals (セキュリティ・IAM)
  - Data Fundamentals (データ基盤)
  - AI Fundamentals: Foundations for Understanding AI (AI)
  - Make Agentic AI Work for You (AI)
- level 充足: 4/4件 — Credly 公式バッジページの Level 表記 (Intermediate ×3、Foundational ×1) を転記
- duration_text 充足: 0/4件 — Credly ページは "Time: Hours / Days" と単位区分のみで数値を出していないため空欄とした (下記参照)
- description: 全件に Credly 公式バッジページの説明文を設定
- 全件とも Credly ページで "Cost: Free" を確認済み

## カバレッジの限界 (正直な報告)

- **カタログ本体 (1,000件超とされる) は列挙できなかった。** skillsbuild.org は JavaScript 描画のみで、テキスト取得ではカタログ中身が一切現れない。さらにコース詳細は無料アカウントでのログインが前提で、公開範囲が限られる。
- そのため本収集は、**ログインなしで公式に検証できる「デジタルクレデンシャル付き学習パス」のうち、Credly 公式バッジページを実際に開いて確認できた4件**に限定した。これは SkillsBuild 全体のごく一部である。
- 存在自体は二次情報で確認できるものの、公式の個別URLを推測なしに特定・検証できなかったため**未収録**とした主なもの: Cloud Computing Fundamentals、Web Development Fundamentals、Information Technology Fundamentals、AI Literacy、AI Fundamentals: Language and Vision in AI、Enterprise Design Thinking Practitioner、Project Management Fundamentals、Career Management Essentials、Be an Entrepreneur、Data Literacy ほか多数。
- 所要時間について: IBM のカタログ側では Cybersecurity Fundamentals 約7.5時間、Data Fundamentals 約7時間、AI Fundamentals は3〜10時間帯、といった見積りが公表されていると各種公開資料が伝えているが、原文を公式ページで直接確認できなかったためレコードには転記していない。
- なお旧名称の "Artificial Intelligence Fundamentals" バッジは Credly に残っているが、現在のカタログでは "AI Fundamentals: Foundations for Understanding AI" に置き換えられているため、現行名称の方を収録した。

## 検証方法

1. skillsbuild.org のカタログ/バッジ紹介ページを実際に開き、JS描画で内容が取得できないことを確認
2. IBM 公式のクレデンシャル発行基盤である Credly の IBM SkillsBuild バッジページを1件ずつ開き、タイトル・説明・レベル・無料表記を確認できたものだけを収録
3. バッジURLは、公式バッジページ間のリンクおよび公式ページへリンクする公開資料から得たものを実際に開いて検証した (組み立て・推測なし)
