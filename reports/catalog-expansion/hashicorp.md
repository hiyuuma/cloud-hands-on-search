# HashiCorp 公式チュートリアル 収集報告

- 収集日: 2026-11-18
- 出力: `data/vendor-staging/hashicorp.json` — **全499件**（tutorial 477件 + collection 22件）、URL重複なし
- 対象: developer.hashicorp.com/tutorials の7製品（Terraform / Vault / Consul / Nomad / Packer / Boundary / Waypoint）

## 製品別件数

| 製品 | 件数 | tutorial | collection |
|---|---|---|---|
| Terraform | 179 | 172前後 | 15（後半コレクションの入口レコード） |
| Vault | 141 | 140 | 1 |
| Consul | 53 | 51 | 2 |
| Nomad | 42 | 38 | 4 |
| Packer | 26 | 26 | 0 |
| Boundary | 50 | 49前後 | 0〜1 |
| Waypoint | 8 | 8 | 0 |
| **合計** | **499** | **477** | **22** |

（tutorial/collection の製品別内訳は概数。総数の 477/22 は実測値）

## 使った公式ページ（出典）

- 製品別チュートリアル索引:
  - https://developer.hashicorp.com/terraform/tutorials
  - https://developer.hashicorp.com/vault/tutorials
  - https://developer.hashicorp.com/consul/tutorials
  - https://developer.hashicorp.com/nomad/tutorials
  - https://developer.hashicorp.com/packer/tutorials
  - https://developer.hashicorp.com/boundary/tutorials
  - https://developer.hashicorp.com/waypoint/tutorials
- チュートリアルライブラリ: https://developer.hashicorp.com/tutorials/library
- 各コレクションページ: `https://developer.hashicorp.com/<製品>/tutorials/<コレクション>`（タイトル・所要時間・説明文の出典）
- 公式サイトマップ: https://developer.hashicorp.com/server-sitemap.xml（個別チュートリアルURLの実在確認）
- 個別チュートリアルページ（対応が曖昧なものについてタイトル照合に使用）

## 検証方法

1. コレクションページを実際に開き、掲載チュートリアルのタイトル・所要時間（例 "14min"）・説明文を取得。
2. 個別URLのスラッグは公式サイトマップ（server-sitemap.xml）に掲載されているものだけを採用。推測URLは作っていない。
3. タイトル⇔スラッグの対応は意味的対応付けを基本とし、曖昧なものは個別ページを開いてタイトル一致を実証した（例: Terraform `secrets/secrets-vault` = "Inject secrets into Terraform using the Vault provider"、`cloud/validation-enforcement` = "Enforce OPA policies using HCP Terraform and Styra"、`cloud/dynamic-credentials-no-code` = "Enable self-service workflows with Vault-backed dynamic credentials"、`providers-plugin-framework/providers-plugin-framework-resource-create` = "Implement resource create and read" ほか）。
4. 複数コレクションに重複掲載されるチュートリアルは canonical URL で1件に統合した（例: Vault の KMIP 系は enterprise/ 配下、Boundary の worker-aware targets は worker-management/ 配下）。
5. 統合時に URL で重複排除し、全レコードの必須フィールド充足と developer.hashicorp.com ドメインであることを機械検証した。

## duration の充足率

- tutorial 477件: **477/477（100%）** にコレクションページ表記の duration_text あり
- 全体では 477/499（95.6%）。残り22件は collection レコードで、コレクション自体に所要時間表記がないため空
- level はコレクションページに表示がなかったため全件 ""（出典にない情報は入れていない）

## カバレッジの限界（正直な申告）

- **Terraform**: 対象コレクション全19+10件を個別チュートリアルまで展開済み。担当コレクション内の掲載分は原則全件対応付けできた。ただし全個別ページを開いての照合はサンプルに留まる（サイトマップ実在＋コレクションページ突合が主）。
- **Vault**: 担当23コレクション中18コレクションは完全収録。一部欠落あり:
  - day-one-raft 7/8（"Harden server deployments" のスラッグ未確認）
  - enterprise 20/23（ライセンス導入、SAML SSO、PKI external policy の3件が未確認）
  - get-started-hcp-vault-dedicated 6/8（2件未確認）
  - vault-agent 5/6（Kubernetes workloads 向け1件未確認）
  - cross-products は個別1/8のみで、残りは collection レコードで代替
  - サイトマップ上に存在する **pki / key-management / kubernetes-introduction / kubernetes-platforms / new-release コレクションは今回未収集**（索引ページのハイライト外だったため担当範囲に入らなかった）
- **Consul / Nomad**: エイリアス系コレクション（developer-discovery、service-mesh-* 等、内容が他と完全重複）は個別追加せず重複排除した。一部の項目はスラッグ対応が確定せず collection レコードで代替（Consul network-automation の consul-template 編、Nomad integrate-consul の API Gateway 編、manage-clusters の Grafana 編、ai-workloads、migrate-monolith の一部）。Consul integrations-vault の2件は canonical URL が Vault 製品側のため Consul としては除外。
- **Boundary**: enterprise コレクションの "Install a HashiCorp Enterprise license" はサイトマップに該当スラッグがなく個別収録を見送り。
- **対象外として意図的に除外**: 旧バージョン系コレクション（Terraform 0-13 / 0-14 / 1-0、Nomad nomad-1-0）、archive コレクション、資格対策コレクション（Terraform certification-004 / pro-cert、Vault associate-cert-003 / ops-pro-cert。手順形式ハンズオンではなく学習ガイド・問題集のため）、validated-patterns（チュートリアルではない）、対象7製品以外の HCP 系チュートリアル（vault-radar 等）。
- 収集作業中、browser.open の並列実行で一時的に 429（レート制限）が発生したため、以降は逐次アクセスに切り替えて完走した。Terraform 後半コレクションは当初 collection レコードのみで提出され、その後コーディネーターが個別展開を追加実施した。

## 分類について

- domain は IaC / ネットワーク / セキュリティ・IAM / コンテナ / その他 から内容に応じて付与（内訳: セキュリティ・IAM 220、IaC 125、コンテナ 72、ネットワーク 49、その他 33）
- priority_for_user はユーザーのテーマ（IaCによるクラウド基盤構築、12月テーマ=ネットワーク/IAM、コンテナ）への近さで 高187 / 中212 / 低100
- summary_ja は出典の英語説明文をもとに作成した1行要約
