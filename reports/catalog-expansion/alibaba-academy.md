# Alibaba Cloud Academy 収集報告（拡充・第2波）

- 収集日: 2026-11-18
- 出力: `data/vendor-staging/alibaba_academy.json`（**13件**）

## 使った公式ページ

- Alibaba Cloud Academy（edu.alibabacloud.com）の各コース詳細ページ `https://edu.alibabacloud.com/course/<id>`
- コース詳細ページを直接開いて確認したもの: 353（Alibaba Cloud Computing Fundamentals）、577（First Look at Alibaba Cloud Generative AI）、52、284、49（除外）
- 残りは検索エンジンが取得した当該公式コースページのクロール内容で確認

## 無料の切り分け方法

- **コース詳細ページ自体に独立した価格ラベル「free」が表示されているコースのみ**を収録した。
- 「Learn for Free (Membership)」表示のコースは**除外**した。メンバーシップは有料プランのため、「無料（Free）明示」には当たらないと判断した（例: コースID 8, 10, 20, 35, 36, 174, 177, 195, 203, 208 など）。
- 除外した検証済みケース:
  - 49 Lab Demo for VPC and Vswitch Creation — ページを開いたが「free」ラベルなし（第三者サイトでは無料とされていたが公式で確認できず除外）
  - 732 Generative AI with Alibaba Cloud — ページは存在するが価格表示を確認できず除外
  - 6 / 78 — 公式 Galaxy Program ページで「FREE USD 10.00」というプロモ価格表示があり判定が曖昧なため除外
  - 221 Function Compute HTTP Trigger デモ — 「free」ラベルなし

## 検証方法

- 全13件のURLは公式コースページの実在を確認済み（直接オープン、または同一公式ページの検索クロール）。URLの推測・組み立てはしていない（IDはすべて実ページから取得）。
- レベル・所要時間は公式ページに明示がなかったため全件空欄とした（推測で埋めていない）。
- description は公式ページの説明文が取得できた2件（52, 147）のみ転記し、他は空欄。

## カバレッジの限界

- カタログ一覧ページ（edu.alibabacloud.com/course/explore）は JavaScript 描画のためテキスト取得ではナビゲーションしか得られず、**全件列挙はできなかった**。収録13件は上限100件を大きく下回るが、これは「free ラベルを公式ページで確認できたものだけ」という厳格な基準の結果である。
- 「Learn for Free (Membership)」コース群（多数存在）を含めれば件数は増えるが、有料メンバーシップ前提のため本波の対象外とした。必要なら別基準（メンバーシップ特典）として再収集が可能。
- ライブブラウザでの追加列挙を行えば網羅性は上がる見込み（本タスクではブラウザ操作なしの制約あり）。
