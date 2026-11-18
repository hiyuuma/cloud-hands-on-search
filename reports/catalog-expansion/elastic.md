# Elastic 学習カタログ収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/elastic.json` (**7件**)

## 使った公式ページ (列挙の母集団・裏取り)

| ページ | URL | 用途 |
|---|---|---|
| Elastic Training トップ | https://www.elastic.co/training | 「Learn Elastic for free」セクション (Search / Observability / Security / Platform の4カテゴリ) と講師主導コースの切り分け |
| 公式ブログ「Elastic's move to free on-demand training」(2025-12-09) | https://www.elastic.co/blog/free-on-demand-training | オンデマンドトレーニングの無料化と、無料モジュールのトピック (ES\|QL for Security 等) の確認 |
| 各モジュールのコースページ (7件) | elastic.json の各 URL | タイトル・説明文の取得と実在確認 |

## 件数と無料確認の根拠

- 収録件数: **7件** (course 6件 + exam 1件、全件 elastic.co/training 配下の個別ページあり)
- 無料であることの確認根拠は2段階:
  - **直接確認できた4件**: トレーニングトップの無料セクション (Search カテゴリ) に明示掲載の Semantic search foundation / Semantic search text embedding / GenAI Associate Accreditation Exam の3件と、公式ブログが無料モジュールの第一弾として挙げた ES|QL for Security (= ES QL for security analysts) の1件
  - **同一形式で収録した3件**: Data types and mappings / Security Quick Start / Getting started: Actions and escalate は、同じオンデマンドモジュール形式のコースページ (Course summary + Topics 構成、価格・開催スケジュールの提示なし) であり、無料セクションの他カテゴリ (Platform / Security) のモジュールと判断して収録した。ただし無料セクション側のタブ内容をテキスト取得では展開できなかったため、この3件は上記4件より確認度が一段低い
- level 充足: 1/7件 (GenAI Associate Accreditation Exam のみ、ページ表記 "Associate level" を転記)
- duration_text 充足: 0/7件 (各モジュールページに所要時間の明記を確認できなかったため全件空欄。推測補完なし)

## 無料/有料の切り分け

- **無料 (収録対象)**: 2025年12月に有料から無料へ移行したオンデマンドの bite-sized モジュール群と、無料・無監督の Associate アクレディテーション試験 (GenAI Associate Accreditation)
- **有料 (収録対象外)**: 講師主導トレーニング **4コース** — Elasticsearch Engineer / Data Analysis with Kibana / Elastic Observability Engineer / Elastic Security for SIEM (開催ページでは受講料の提示あり。例: Elastic Security for SIEM / for Endpoint は 2,700 USD、Elasticsearch Engineer は 2,500 EUR の開催回を確認)。認定試験プログラム (Elastic Certified Engineer 等) も有料側

## カバレッジの限界 (正直な報告)

- トレーニングトップの無料セクションはタブ切替形式で、テキスト取得では Search カテゴリの5件しか展開できなかった。Observability / Security / Platform カテゴリの全モジュール一覧は取得できていない
- 無料セクション掲載が確認できたのに個別ページ URL を特定できず**収録を見送った2件**: 「Getting started: What is Elastic?」「RAG foundation」(タイトルは公式ページで確認済み。URL の推測・組み立ては行わない方針のため除外)
- 公式ブログが無料モジュールのトピックとして挙げた Attack Discovery / Elastic AI Assistant / Elastic AI SOC Engine (EASE) / Elastic logs essentials も、個別ページ URL を特定できず未収録
- モジュールの実体は学習ポータル learn.elastic.co (ログイン必須の LMS) で提供される。収録 URL は elastic.co 側の公式コース紹介ページであり、そこから受講導線が張られている
- 各コースページの本文はテキスト取得ではヘッダ部分しか返らなかったため、説明文は検索インデックスに残る同ページの "Course summary" を転記し、タイトルは実際にページを開いて照合した

## 検証方法

1. 母集団の確定: トレーニングトップの無料セクションと公式ブログで、無料プログラムの範囲 (カテゴリとモジュール名) を確認
2. URL の取得: 各モジュールの URL は検索結果として返された elastic.co 公式 URL をそのまま使用 (組み立て・推測なし)
3. 実在確認: 全7件について実際にページを開き、応答タイトルがモジュール名と一致することを確認した
