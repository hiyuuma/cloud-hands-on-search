# SAP Learning 収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/sap_learning.json` (**17件**、全て course)

## 使った公式ページ

- SAP Learning: https://learning.sap.com/learning-journeys (一覧は JS 描画で機械取得不可。本文確認用)
- 各コースページ https://learning.sap.com/courses/<slug> の「About this course」(学習目標、Prerequisites、Roles/products) が検索インデックスに保持されており、それを出典とした
- 実在確認として「Getting Started with SAP Forms Service by Adobe」を実際に開き、タイトル・About・前提コース・ロール (Developer, SAP BTP/ABAP environment) の一致を確認した
- 補助出典: IDES24 の調査 (2026-11-16 時点で Learning Journey 187件が掲載、レッスンは登録なしでも閲覧可=無料) と SAP Community の Learning Journey 紹介記事

## 範囲と単位について

- 現在の learning.sap.com では Learning Journey の内容は /courses/ 配下のコースページとして提供される形に移行しており、本収集の単位はコースとした (一部コースの About には "After completing this learning journey" と併記されている)
- 優先順位: AI (Joule 系4件) と開発 (ABAP/CAP/Fiori/Build Code 5件) を厚めにし、S/4HANA 基礎・導入系とクラウド基礎を加えた
- 無料の線引き: learning.sap.com のレッスン閲覧は無料 (演習システムや認定試験はサブスクリプション側) という公式提供形態に基づき、同サイトのコースを無料教材として収録した

## 件数と充足率

- level 充足: 1/17件 (Exploring SAP Cloud ERP の "Beginner Level" のみ出典明記)
- duration_text: コースページに総所要時間の原文表示を確認できず全件空欄 (レッスン単位の時間はあるが合算は推測になるため入れていない)
- description: 全件に公式 About の学習目標を設定

## カバレッジの限界 (正直な報告)

- 母数は Learning Journey 約187件 (2026-11 時点の第三者調査) + コース群で、本収集の17件は上限100件にも届かない一部である
- 一覧が JS 描画で列挙できず、検索インデックスにコーストップページが載ったものだけを収録した。レッスンページ (/courses/<slug>/<lesson>) しかインデックスされていないコースは、トップ URL を推測で作らないため除外した (例: Becoming an SAP BTP Solution Architect)
- 「Learning the Basics of ABAP Programming on SAP BTP」はインデックスに載ったのがドイツ語ロケール版 URL (-de) だったため、その URL をそのまま記録し description に注記した
- 「Setting Up Joule Across your Organizational System Landscapes」は SAP 公式発信に使われたトラッキングパラメータ付き URL をそのまま転記した

## 検証方法

1. learning.sap.com のコースページがインデックスに保持した About 本文でタイトル・内容の対応を確認
2. 代表1件を実際に開いて全文と突合
3. URL は提示された完全な URL をそのまま転記し、組み立て・推測はしていない
