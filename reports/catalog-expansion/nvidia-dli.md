# NVIDIA DLI 収集報告（拡充・第2波）

- 収集日: 2026-11-18
- 出力: `data/vendor-staging/nvidia_dli.json`（**11件**、全て無料セルフペースド）

## 使った公式ページ・資料

- learn.nvidia.com の各コース詳細ページ（URLは下記方法で実物を取得し、全11件中10件は実際に開いて解決を確認）
- NVIDIA 公式「Training Course Catalog」PDF（2026年10月版、NVIDIA CDN 配布）— Agentic AI Explained「1 Hour / Free」、Securing Agents With NemoClaw and OpenShell「4 Hours / Free」を原文確認
- docs.nvidia.com/learn-openusd（Learn OpenUSD 公式ドキュメント）— 「free, open-source learning path」であることを公式ページで確認
- 列挙の起点として、公式カタログを精査した第三者ガイド2件（2026-10-04 時点再確認の jasonzhu.ai、2026-10-17 時点の pasqualepillitteri.it ガイド）を使用し、両者の一致を確認した上で公式資料で裏付けた

## 無料の切り分け方法

- DLI カタログ（全52コース = セルフペースド26 + インストラクター主導26）のうち、価格が **Free** のセルフペースドコースのみ収録。
- 2026年10月の再確認で一致した無料11件: エージェントAI 2件、ロボティクス 3件、Omniverse/OpenUSD 6件（うち1件は docs.nvidia.com の学習パス）。
- 注意: 旧来「無料」と紹介されがちなコース（Building RAG Agents with LLMs、Fundamentals of Accelerated Computing with CUDA Python、Generative AI Explained 等）は現在 **$90 または提供終了** であり、収録していない。

## 有料分（件数のみ報告）

- 有料セルフペースド: **15件**（$30 × 7、$90 × 8）
- インストラクター主導ワークショップ: **26件**（公募席は $500〜）
- 認定試験: 13件（$125〜$500、カタログ52コースとは別枠）

## 検証方法

- learn.nvidia.com のコースURL（course_id）は推測せず、ガイド内リンクの実解決（実際に開いて遷移先URLを取得）により10件分を取得した。
- learn.nvidia.com のコースページ本体は JavaScript 描画でテキスト取得できないため、所要時間・レベル・説明は公式カタログPDF（2件）および公式ページ精査ガイド2件の転記で補った。Learn OpenUSD の説明は公式ドキュメントの原文。
- Fundamentals of Deep Learning は DLI カタログ外の無料オープンソース教材（GitHub: NVDLI/fundamentals-of-deep-learning、修了証なし）のため本ファイルには含めていない。

## カバレッジの限界

- 無料コースのラインナップは変動が激しい（2026年だけでも複数コースが有料化・終了）。本収録は2026-10〜11時点の確認に基づく。
- spectrumailab の調査（2026-07確認）では「Generative AI and LLM 学習パスページに公式フィルタに出ない無料コースが10件程度ある」と指摘されている。今回の基準（DLIカタログの Free 表記）では対象外としたため、厳密な「全無料」ではない。この点は統合時に判断されたい。
