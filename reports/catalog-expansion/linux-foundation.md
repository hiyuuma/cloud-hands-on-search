# Linux Foundation / CNCF カタログ収集報告

- 収集日: 2026-11-18
- 出力: `data/vendor-staging/linux_foundation.json`（59件）
- 対象: Linux Foundation 公式トレーニング（training.linuxfoundation.org）

## 使った公式ページ

- Cloud & Containers カテゴリページ（価格・レベル・種別の一覧）: https://training.linuxfoundation.org/cloud-containers/
- フルカタログ（Cloud & Containers 絞り込み）: https://training.linuxfoundation.org/full-catalog/?_sft_topic_area=cloud-containers
- 認定カタログ（System Administration / Systems Engineering 絞り込み）: https://training.linuxfoundation.org/certification-catalog/?_sft_topic_area=system-administration,systems-engineering
- 認定パス一覧: https://training.linuxfoundation.org/learning-paths/
- 各商品ページ（コース /training/<slug>/、認定 /certification/<slug>/、Express Learning /express-learning/<slug>/）を個別に開いてタイトルと URL の対応を確認

## 件数と内訳

- 総件数: **59件**
  - course: 40件（eラーニング 30件、講師主導 ILT 4件、1日ワークショップ LFWS 4件、Express Learning 1件、ほか Linux 系 eラーニング）
  - certification: 17件（CKA / CKAD / CKS / KCNA / KCSA / CKNE / CNPA / CNPE / PCA / ICA / CAPA / CCA / KCA / OTCA / CBA / LFCS / LFCA）
  - bundle: 2件（CKA+CKAD+CKS 試験バンドル、CKNE Certification Pathway）
- 価格内訳（公式ページ表示ベース）
  - 無料（$0）: 9件（LFS158, LFS146, LFS144, LFS147, LFS148, LFS140, LFS157, LFEL1014, LFS101）
  - 有料（価格確認済み）: 44件
  - 価格未取得: 6件（LFCS, LFCA, LFS200, LFS203, LFS307, LFD201。商品ページのテキスト抽出に価格表示が含まれなかったため空欄。推測では埋めていない）

## 検証方法

- 全59件について、公式カタログページ上のリンクを実際にたどって商品ページを開き、ページタイトルと URL の一致を確認した（URL の推測生成はしていない）
- 価格・レベルは公式カテゴリページ（Cloud & Containers）の一覧表示、および各商品ページ本文から転記した
- 認定試験は type=certification として区別した。CKA/CKAD/CKS/LFCS は実技（パフォーマンスベース）試験、Associate 系は多肢選択が中心で、学習教材そのものではない点に注意

## カバレッジの限界

- 優先分野（Kubernetes / コンテナ / クラウドネイティブ / Linux システム管理）に絞った。LF 公式カタログ全体は 150+ 商品あり、以下は対象外とした
  - 日本語版（-JP）の重複商品（CKA-JP 等）、ドイツ語版、THRIVE-ONE サブスクリプション付きバンドル、Kubestronaut 系バンドル、SkillCred（SC100〜SC109 の小規模クレデンシャル）、RISC-V / Blockchain / FinOps 等の周辺分野
  - LFCE（Linux Foundation Certified Engineer）は現在の認定パス一覧（10認定）に掲載がなく、現行の公式商品ページを確認できなかったため収録していない
- duration_text は公式ページに明記があるもののみ（1日ワークショップ、試験時間の一部）。eラーニング各コースの標準学習時間は商品ページに一貫した記載がなく、大半は空欄
- 取得作業中にブラウザ取得のレート制限（429）に複数回当たったため、検証は商品ページ単位で間隔を空けて実施した。WordPress API（wp-json）経由の一括取得はタイムアウトしたため使用していない
- 価格は 2026-11-18 時点の表示。LF はセール（例: サイト全体 40% off 等）を頻繁に行うため、実購入時は再確認が必要
