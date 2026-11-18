# Red Hat Developer 収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/redhat_developer.json` (**12件**)

## 使った公式ページ

| ページ | URL | 用途 |
|---|---|---|
| Red Hat Interactive Learning Portal | https://developers.redhat.com/learn | ポータル全体の構成確認 (製品フィルター一覧) |
| OpenShift learning | https://developers.redhat.com/learn/openshift | OpenShift 系の注目ラーニングパス列挙 |
| Ansible Automation learning | https://developers.redhat.com/learn/ansible | Ansible 系ラーニングパスの列挙 |
| Foundations of OpenShift | https://developers.redhat.com/learn/openshift/foundations-openshift | 詳細ページを実地で開いて確認 (12 resources / 3 hrs and 40 mins) |
| OpenShift Container Platform Tutorials (Additional hands-on learning) | https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/ (Tutorials) | Red Hat Developer ラーニングパスの公式一覧表 (タイトル・説明の裏取り) |

各レコードの詳細 (種別・リソース数・所要時間・説明文) は、developers.redhat.com の各詳細ページの掲載内容 (検索インデックス経由で全文確認できたものを含む) に基づく。URL は公式ページ・公式ドキュメントに現れたものをそのまま使用し、推測で組み立てていない。

## 件数と内訳

- 収録件数: **12件** (すべて type=learning-path)
  - OpenShift: 3件 (Foundations of OpenShift / Learn Kubernetes using the Developer Sandbox / Store persistent data in Red Hat OpenShift using PVCs)
  - Ansible: 5件 (Foundations of Ansible / Get started with Ansible Playbooks / Getting started with Ansible Content Collections / Get started with the Ansible Visual Studio Code extension / Integrate Red Hat Developer Hub with Red Hat Ansible Automation Platform)
  - RHEL: 4件 (image mode 系 3件 / Lightspeed 堅牢化 1件)
- duration_text 充足: 5/12件 (「3 hrs and 40 mins」「2 hrs and 28 mins」「1 hr and 20 mins」「40 mins」「30 mins」— 出典ページの原文どおり)
- level 充足: 0/12件 (出典ページにレベルの明示がないため全件空欄。推測補完なし)

## 無料性の確認

- Red Hat Developer のラーニングパスは Red Hat アカウント (無償の Developer 登録) で利用でき、OpenShift 系は無償の Developer Sandbox クラスタを使う構成であることを各ページの前提条件で確認した。
- Ansible 系の一部は前提条件に「Ansible Automation Platform のサブスクリプション (無償トライアル可)」とある。教材自体は無償で閲覧できるが、実習環境にトライアル登録が必要な場合がある点は留意事項とする。

## カバレッジの限界

- developers.redhat.com/learn には数百件規模のラーニングパス/インタラクティブチュートリアルがある。本収集は指示範囲 (OpenShift、Ansible、Linux) の代表的な 12 件に限る選抜収録であり、全件列挙ではない。OpenShift AI、Developer Hub、Kafka、Quarkus 等の他トピックは対象外とした。
- OpenShift 系の旧パス (Using OpenShift、Container Fundamentals、Developing applications on OpenShift、How to deploy full-stack JavaScript applications in OpenShift) は Red Hat 公式ドキュメントの一覧表に現行掲載があるものの、Using OpenShift の旧 URL (…/learn/openshift/using-openshift) を開くとハブページへリダイレクトされ詳細を確認できなかったため、URL を実地確認できた 3 件のみ収録した。
- 「Learn Kubernetes using the Developer Sandbox」の URL は、検索結果に現れたトラッキングパラメータつきのものをそのまま採用した (パラメータを除いた形は未検証のため改変していない)。
- インタラクティブチュートリアル (例: Deploy containers with Podman) は存在を確認したが、個別 URL の実地確認に至らず未収録。
- ページ取得 API のレート制限 (429) のため、詳細ページの直接確認は Foundations of OpenShift とハブ 2 ページに留め、残りは公式詳細ページの検索インデックス掲載内容 (種別・リソース数・所要時間・説明文を含む) で検証した。

## 検証方法

1. 列挙: ポータルのトピック別ハブ (OpenShift / Ansible) と RHEL 関連の検索で候補を列挙
2. URL の取得: 公式ハブ・公式ドキュメント・検索結果に現れた developers.redhat.com/learn 配下の URL をそのまま転記 (組み立て・推測なし)
3. 実在確認: Foundations of OpenShift は詳細ページを実際に開いてタイトル・種別・所要時間・説明の一致を確認。その他は公式詳細ページの掲載内容 (タイトル・Learning path 表記・リソース数・所要時間・説明文) と突合した
4. 所要時間・レベルは公式ページに原文がある場合のみ転記し、無い場合は空欄にした
