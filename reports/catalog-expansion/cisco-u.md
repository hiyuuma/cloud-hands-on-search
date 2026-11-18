# Cisco U. 収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/cisco_u.json` (**4件**)

## 使った公式ページ

| ページ | URL | 用途 |
|---|---|---|
| Cisco U. Free Learning Path titles (公式の無料パス一覧) | https://u.cisco.com/titles/Free_Titles | 無料パスの母集団 (23件)・レベル・概要の取得 (2026-11-18 取得) |
| Cisco U. パス一覧 | https://u.cisco.com/paths?type=labs | Free バッジ付きパスの確認 |
| Cisco Learning Network 公式ブログ (May 2026 / Nov 2025) | learningnetwork.cisco.com | CML系3パスの無料化と所要時間の裏取り |
| Cisco 公式 Facebook (12 Days of Learning) | facebook.com/learningatcisco | NETFND の FREE バッジ・14時間の確認 |
| 各パスページ (4件) | u.cisco.com/paths 配下 (JSON の url 参照) | 個別 URL の実在確認 |

## 件数と内訳

- 収録件数: **4件** (全件 type = `learning-path`)
  - Network Fundamentals for Network Adjacent Engineers (NETFND) — Beginner / 14 hours / priority 高
  - Introduction to Network Simulations with Cisco Modeling Labs (CMLLAB) — Beginner / 8h 30m / 中
  - Understanding Cisco Network Automation Essentials (DEVNAE) — Intermediate / 28h 40m / 中
  - Administering Cisco Modeling Labs (CMLADM) — Intermediate / 4h 30m / 低
- domain: 全件 `ネットワーク` / services: Cisco (CML系は Cisco Modeling Labs を併記)

## 無料の切り分け方法

- Cisco U. のパス一覧で **Free バッジが明示されたもの**、および公式の無料タイトル一覧ページ (Free_Titles) に掲載されたものを「無料」とした
- 期間限定の無料プロモーション (例: Rev Up to Recert の AITECH / AIBIZ、2026-02-09〜03-26) は常時無料と区別し、単独では根拠にしていない。なお Cisco AI Business Practitioner は 2026-11-18 時点で Free_Titles 一覧に掲載されている (下記19件リスト参照)

## 検証方法

1. 母集団: 公式 Free_Titles ページに載る無料ラーニングパス全23件を列挙 (タイトル・レベル・CE クレジット・テクノロジー・概要は同ページの公式表記のまま下表に転記)
2. 個別 URL: パス個別ページの URL が公式ページまたは公式発信で **一字一句確認できた4件のみ** を JSON に収録した。Cisco U. のパス URL は数値 ID 型 (`/paths/243`) とスラッグ+ID 型 (`/paths/administering-cisco-modeling-labs-240`) が混在し、タイトルからの推測ができないため、未確認のものは収録していない

## カバレッジの限界 (重要)

- **公式に無料と確認できた23件のうち、個別 URL が検証できたのは4件のみ**。残り19件は下表のとおり実在と無料が公式一覧で確認できているが、直接リンク未検証のため JSON 未収録。Oracle 第1波→ブラウザ追加収集で回収したのと同様、**ライブブラウザで u.cisco.com を巡回すれば回収できる見込み** (パス一覧は JavaScript 描画で、テキスト取得では個別 URL が得られない)
- 無料タイトル一覧 (Free_Titles、2026-11-18 取得、全23件):

| # | Title | Level | CE | Technology |
|---|---|---|---|---|
| 1 | Administering Cisco Modeling Labs | Intermediate | 5 | Networking |
| 2 | Advanced Automation with Cisco Modeling Labs | Intermediate | 8 | Networking |
| 3 | AI Agent Fundamentals | Beginner | 0 | Other |
| 4 | AI Foundations for Legal Professionals | Beginner | 0 | Software |
| 5 | Application Performance Monitoring Essentials for Cisco AppDynamics | Beginner | 0 | Application Performance |
| 6 | CCNA Learning Preview | Beginner | 0 | Networking |
| 7 | CCSI Fundamentals | Advanced | 0 | (複数領域) |
| 8 | Cisco AI Business Practitioner | Beginner | 8 | Software |
| 9 | Cisco Energy Networking Systems and Panduit Fault Managed Power | Beginner | 0 | Networking |
| 10 | Cisco Provider Connectivity Assurance - Analytics | Advanced | 0 | Networking |
| 11 | Cisco Provider Connectivity Assurance - Introduction | Beginner | 0 | Cloud and Computing, Networking |
| 12 | Cisco Provider Connectivity Assurance - Orchestrator | Intermediate | 0 | Cloud and Computing, Networking |
| 13 | Cisco Provider Connectivity Assurance - Performance Elements | Intermediate | 0 | Networking |
| 14 | Cisco Provider Connectivity Assurance - Sensor Control | Intermediate | 0 | Cloud and Computing, Networking |
| 15 | Cisco ThousandEyes Essentials | Beginner | 0 | Networking |
| 16 | Designing and Implementing Cisco Service Provider Cloud Network Infrastructure | Intermediate | 40 | Networking |
| 17 | Evolution of Cisco Network Operating Systems | Beginner | 0 | Networking |
| 18 | Introduction to Network Simulations with Cisco Modeling Labs | Beginner | 6 | Networking |
| 19 | Network Fundamentals for Network Adjacent Engineers | Beginner | 0 | Networking |
| 20 | Securing Industrial IoT Networks with Cisco Technologies | Intermediate | 0 | Internet of Things (IoT) |
| 21 | Understanding AI and LLMs as a Network Engineer | Beginner | 0 | Networking |
| 22 | Understanding Cisco Network Automation Essentials | Intermediate | 16 | Networking, Software |
| 23 | Understanding Cisco Ultra-Reliable Wireless Backhaul Foundation | Beginner | 0 | Networking |

  収録済みは #1, #18, #19, #22。未収録19件のうち優先度が高い候補: #2 Advanced Automation with Cisco Modeling Labs (CMLAPI、7h 55m)、#21 Understanding AI and LLMs as a Network Engineer (AI4NE)、#6 CCNA Learning Preview (3h 30m)、#3 AI Agent Fundamentals (AGTFNDU、2h 34m)
- Cisco U. には無料のチュートリアル/コース単体も多数あるが、本収集はラーニングパスに限定した (Free_Titles がパス単位の一覧のため)。コース・チュートリアル単位の収集は未実施
- 無料区分は変動しうる (CML系3パスは 2025-11 に有料から無料化された)。Free_Titles ページ自体が「This Learning Path list is subject to change」と明記している

## 追補 (2026-11-18、ブラウザ追加収集)
実ブラウザで残り19パスの詳細ページを全件確認し cisco_u.json に追加 (計23件 = Free_Titles 全件)。AI Agent Fundamentals は旧ID 21311 が一覧へリダイレクトされ、正しいID 21543 を確認。注意事項: Cisco ThousandEyes Essentials は詳細ページに「Retired July 28, 2026」表示 (ページ閲覧可、優先度は低に設定)。SPCNI は「Free until Dec 10, 2026」の期間限定無料表示。分類は司令塔 (Muse) が付与。
