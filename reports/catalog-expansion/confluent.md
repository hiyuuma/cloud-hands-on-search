# Confluent 学習カタログ収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/confluent.json` (**27件**)

## 使った公式ページ (列挙の母集団・裏取り)

| ページ | URL | 用途 |
|---|---|---|
| Confluent Developer コース一覧 | https://developer.confluent.io/courses/ | 無料コースの列挙母集団 (25コースを掲載) |
| Confluent Training & Certification | https://www.confluent.io/training/ | 有料側 (講師主導・認定) の切り分け確認 |
| 各コースの導入モジュールページ (27件) | confluent.json の各 URL | タイトル対応と実在の個別確認 |

## 件数と充足率

- 収録件数: **27件** (すべて type=course、全件無料)
  - コース一覧掲載の25件 + 一覧には載っていないが Flink 101 ページから公式リンクされていた2件 (Apache Flink® Table API: Processing Data Streams in Java / Building Apache Flink Applications in Java)
- duration_text 充足: 6/27件 — コースページに "Length" として明記されていたもののみ原文転記 (例: "Approximately 3 hours")。モジュール単位の時間しかないコースは推測で合計せず空欄
- level 充足: 0/27件 — 一覧ページには Fundamentals / Intermediate / Advanced のフィルタ区分はあるが、取得できたテキストではコース個別のレベル表記を確認できなかったため、全件空欄 (推測補完なし)
- description: 全件にコース一覧ページの公式説明文 (長いものは冒頭を抜粋) を設定

優先度 (priority_for_user) の付け方: ストリーミングはデータ基盤の実務テーマのため、入門・実践とも「中」。手法論寄りの Practical Event Modeling と、対象が狭い CSFLE の動画シリーズのみ「低」。

## 無料/有料の切り分け

- **無料 (収録対象)**: Confluent Developer (developer.confluent.io) のコースは全件無料。演習で Confluent Cloud を使うコースも、プロモコードによる無料クレジットで実施できる旨が各コースページに明記されている
- **有料 (収録対象外)**: confluent.io/training が案内する講師主導トレーニング (カタログは training.confluent.io で提供) と認定試験 (CCDAK / CCAAK / Confluent Certified Cloud Operator の3認定、および Fundamentals 系アクレディテーション2種)。講師主導コースの個別件数は、training.confluent.io のカタログが JavaScript アプリでテキスト取得できず、正確な件数は確認できなかった (種別としては講師主導コース群 + 認定試験が有料側の全体)

## カバレッジの限界 (正直な報告)

- 母集団は Confluent Developer のコース一覧 (25件) を正とした。同サイトにはコース以外にもチュートリアル、ハンズオン、ドキュメント等の学習コンテンツがあるが、本収集は「コース」形式に限った
- 収録 URL は各コースの導入モジュールページ (コース開始点) のもの。サイトの構造上、コースのトップ URL は導入モジュールへ誘導されるため、この形が実際の導線になる
- "Kafka for Python Developers" のタイトルはコース一覧の公式リンク表記を採用した (モジュールページ側の見出しは "Introduction to Python for Kafka")

## 検証方法

1. 母集団の列挙: Confluent Developer 公式コース一覧でタイトルと説明文を列挙
2. URL の取得: 一覧ページの各コースリンクを実際に辿り、遷移先として返された URL をそのまま転記 (組み立て・推測なし)
3. 実在確認: 全27件について遷移先ページが応答し、内容が当該コースのものであることを確認。所要時間はコースページに "Length" 表記がある場合のみ転記した
