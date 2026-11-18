# Oracle (OCI) 学習カタログ収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/oracle_oci.json` (**15件**)

## 使った公式ページ (列挙の母集団・裏取り)

| ページ | URL | 用途 |
|---|---|---|
| Oracle IaaS Training and Certification (Oracle University 公式カタログ) | https://education.oracle.com/pt_BR/navega%C3%A7%C3%A3o-na-vitrine/iaas/pPillar_640 | OCI 学習パスの一覧 (Administrator / Developer / Architect 別、全29タイトル) を列挙する母集団として使用 |
| Oracle MyLearn "Free Training and Certifications from Oracle University" | https://mylearn.oracle.com/ou/story/35573 | Foundations 系パスと所要時間 (Agentic AI 6h 51m、Cloud Business Jumpstart 1h 22m、Cloud Tech Jumpstart 3h 26m) の出典 |
| Oracle MyLearn "Discover AI: Training for Beginners and Beyond" | https://mylearn.oracle.com/ou/story/35644-ai-1/ | OCI AI Foundations Associate の所要時間 (8h 23m) の出典 |
| Oracle University Blog: OCI Certification Learning Paths and Exams 2026 Updates | https://blogs.oracle.com/oracleuniversity/oci-certification-learning-paths-and-exams-2026-updates-now-available | 2026年版ラインナップ (Agentic AI トラック、Database@AWS/Azure/GCP、名称から年号を外した新体系) の確認 |
| Oracle University Blog: OCI 2025 Certification Learning Paths and Exams Now Available | https://blogs.oracle.com/oracleuniversity/oci-2025-certification-learning-paths-and-exams-now-available | 2025年版ラインナップ (Architect/Security/Observability/Migration/Multicloud 等) の確認 |
| Oracle University Blog: OCI Multicloud Architect Certification and Course | https://blogs.oracle.com/cloud-infrastructure/oci-multicloud-architect-certification-and-course | Multicloud Architect パスの内容確認 |
| Oracle University Blog: OCI 2025 Networking Professional | https://blogs.oracle.com/oracleuniversity/oracle-university-launches-the-oci-2025-networking-professional-certification-and-learning-path | Networking Professional パスの存在確認 (URL は下記理由で未収録) |
| Oracle LiveLabs Home | https://livelabs.oracle.com/ords/r/dbpm/livelabs/home | ハンズオン・ワークショップの存在確認 (個別 URL は下記理由で未収録) |

各レコードの URL は、上記公式ページ群および Oracle 公式ドメイン (mylearn.oracle.com / learn.oracle.com) へのリンクを実際に辿って得たものをそのまま使用した。URL の推測・組み立ては行っていない。

## 件数と充足率

- 収録件数: **15件** (learning-path 12件 / course 3件)
- level 充足: 9/15件 (60%) — Foundations 系と Professional 系は出典に明記あり。Jumpstart 系・クロスクラウド系 (OCI for Azure/AWS/GCP Architects) ・Multicloud Architect は公式ページにレベル表記がなく空欄
- duration_text 充足: 4/15件 (27%) — MyLearn の一覧ページに所要時間が表示される項目のみ原文 (例 "6h 51m") を転記。パス詳細ページは JavaScript レンダリングのためテキスト取得では所要時間を確認できず、推測値は入れていない
- description: 全件に公式ページの説明文 (要約含む) を設定

優先度 (priority_for_user) の付け方: 2026-11 テーマ「コンテナ/Kubernetes」→ OKE Specialist と DevOps Professional コースを「高」。12月テーマ「ネットワーク/閉域/IAM」と通年テーマ「エージェント/MCP」→ IAM/VCN を含む Foundations / Architect Associate と、MCP を明示的に扱う Agentic AI Foundations を「高」。OCI 基盤の基礎全般は「中」、ビジネス入門と GCP 向けクロスキルは「低」。

## カバレッジの限界 (正直な報告)

- **母数の推定**: education.oracle.com の公式 IaaS カタログには OCI 学習パスが **29タイトル** (重複除く) 掲載されている。これに 2026年追加分 (Agentic AI Foundations、Enterprise AI Professional、AI Database Foundations、Oracle Database@AWS/Azure/Google Cloud Architect Professional 等) と、認定に紐づかない単体コース・Jumpstart 系が加わる。さらに Oracle LiveLabs には OCI 関連ハンズオン・ワークショップが数百件規模で存在する。したがって本収集の15件は「OCI 認定系学習パスの主要どころ」に限られ、**カタログ全体の網羅ではない**。
- **未収録 (タイトルは公式に確認済みだが URL を検証できず除外したもの)**: OCI Architect Professional / OCI Security Professional / OCI Networking Professional / OCI Developer Professional / OCI Data Science Professional / OCI Generative AI Professional / OCI Observability Professional / OCI Enterprise AI Professional / Autonomous Database Professional / Oracle Cloud Database Service Professional / Oracle Cloud Database Migration and Integration Professional / Oracle Machine Learning with Autonomous Database Associate / Digital Assistant Professional / Oracle APEX Foundation / Oracle APEX Developer Professional / Application Integration Professional / Oracle Cloud Platform Enterprise Analytics Professional / CyberSecurity and Oracle Cloud / Oracle Database@Azure Specialist / Oracle Cloud Data Management Foundations / Oracle AI Vector Search Professional / OCI Multicloud Architect Professional。
  - 除外理由: MyLearn の詳細ページは JavaScript レンダリングで、テキスト取得では本文・所要時間を取得できない。2025年版パスの一部は 2026-09-30 でアーカイブされたことが公式に案内されており、旧 URL が現行有効か判別できないものもあった (例: Networking Professional 2025 のパス URL はリンク先として存在したが取得できず、現行 2026 版の URL は特定できなかった)。「URL は実在確認したものだけ」という制約を優先し、これらは収録しなかった。
- **LiveLabs の個別ワークショップ**: 一覧ページ (livelabs.oracle.com) は取得できたが、テキスト抽出では個別ワークショップの URL が得られなかったため、今回は1件も収録していない。ハンズオン単体を厚くしたい場合は、ブラウザ操作で LiveLabs カタログを辿る追加収集が必要。

## 検証方法

1. 母集団の列挙: education.oracle.com 公式 IaaS カタログページと Oracle University 公式ブログ (2025/2026 ラインナップ発表) で OCI 学習パスのタイトルを列挙
2. URL の取得: MyLearn 公式ページの検索インデックス掲載、Oracle 公式ブログ内のリンク、Oracle の公式学習 URL (learn.oracle.com/ols/…) のリンクを辿り、表示された URL をそのまま転記 (組み立て・推測なし)
3. 実在確認: 取得した URL を実際に開き、ページが応答すること、およびタイトルが公式表記と対応することを確認。応答が確認できなかったもの (アーカイブ済みの疑いがあるものを含む) は収録から除外し、上記「未収録」に理由つきで記録した
4. 所要時間・レベルは公式ページに原文がある場合のみ転記し、無い場合は空欄にした

## 追補 (2026-11-18、ブラウザ追加収集 — ユーザー承認済み)

実ブラウザで MyLearn / LiveLabs を辿る追加収集を実施し、oracle_oci.json は 15件 → **89件** になった。

- MyLearn: 未収録22件中 **13件** の現行パスURLを特定し、詳細ページを開いてタイトル一致と所要時間を確認 (Architect Professional 26h30m、Networking 19h40m 等)。Security Professional は日本語2026年版のみ確認。9件は複数検索でも同名パスが現れず NOT FOUND のまま (検索2ページ目以降に存在する可能性は残る)。Autonomous Database Professional と Database@Azure Specialist は現行版で改称されていた。
- LiveLabs: OCI 関連 **61件** のワークショップを詳細ページで確認 (MCP と OCI Container Instances のエージェント系、OCI Core Services 入門、IAM 統合などを含む)。カタログ全体927件・OCI絞り込み201件中の61件で、上限120件には未達。
- LiveLabs の URL は開いた際の URL からセッション固有パラメータ (session=...) を除去し、安定IDである wid の形 (view-workshop?wid=<id>) で記録した。除去は同一ページへの導線のままである。
- 分類 (domain / services / priority_for_user / summary_ja) は司令塔 (Muse) が付与した。
