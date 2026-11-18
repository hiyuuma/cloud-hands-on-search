# KubeAcademy 収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/kubeacademy.json` (**6件**)

## 最重要の注意: プラットフォームは公式に引退済み

- kube.academy の各ページに **「KubeAcademy has been officially retired on the 1st of January 2026」** の告知が表示される (VMware/Broadcom による KubeAcademy の終了)。
- コース一覧ページ (https://kube.academy/courses) はテキスト取得では「No courses currently available」と表示され、カタログとしての現行運用は終了している。
- 個別コースページの一部は現在も内容 (タイトル・レベル・説明・アウトライン) を表示するが、Kubernetes 101 のページには **「Deprecated — This course has been retired. We suggest the Kubernetes Core Concepts Learning Path instead」** と明記されている。Containers 101 のページは内容を表示せず引退告知のみにフォールバックしたため未収録。
- したがって本収集は「引退済みプラットフォームに残存する検証可能なページ」の記録であり、**カタログへの採用可否は親エージェント/ユーザーの判断を仰ぐべき**。採用する場合も、各コースの受講可否 (レッスン再生) までは未検証である。

## 使った公式ページ

| ページ | URL | 用途 |
|---|---|---|
| Kubernetes Core Concepts (Learning Path) | https://kube.academy/paths/kubernetes-core-concepts | パスの説明文を実地確認 |
| Courses 一覧 | https://kube.academy/courses | 「No courses currently available」を確認 (カタログ終了の根拠) |
| Interactive Introduction to Containers and Kubernetes | https://kube.academy/courses/interactive-introduction-to-containers-and-kubernetes | タイトル・レベル・説明を実地確認 |
| Helm 101 | https://kube.academy/courses/helm-101 | タイトルとコースアウトライン (10レッスン) を実地確認 |
| How to Prepare for the CKA Exam | https://kube.academy/courses/how-to-prepare-for-the-cka-exam | タイトルとコースアウトライン (9レッスン) を実地確認 |
| Kubernetes 101 | https://kube.academy/courses/kubernetes-101 | タイトル・レベル・説明と Deprecated 表示を実地確認 |
| Kubernetes in Depth | https://kube.academy/courses/kubernetes-in-depth | タイトル・レベル・説明を実地確認 |

補助列挙 (タイトルとレベルの裏取り): VMware 公式ブログの KubeAcademy 紹介記事、docs.saltlabs.tech の KubeAcademy コース一覧 (レベル別・所要時間つき)。URL 自体は上記の実地確認済みページのみ採用した。

## 件数と充足率

- 収録件数: **6件** (course 5件 / learning-path 1件)
- level 充足: 3/6件 (出典ページに Beginner 表示があったもののみ)
- duration_text 充足: 0/6件 (個別ページに総所要時間の明示がなかったため空欄。Helm 101 はアウトラインの動画合計約105分、CKA 対策は約120分だが、出典の総時間表記ではないため転記していない)

## カバレッジの限界

- KubeAcademy には本来 30+ コースと 3 ラーニングパスがあったとされる (iximiuz のプラットフォーム紹介等)。Networking in Kubernetes、Kubernetes Platform Security、Building Applications for Kubernetes、Interacting with Kubernetes、Hands-On with Kubectl、Operational Considerations for Virtual Infrastructure Administrators、他の 2 パス (Understanding Cloud Native / Introduction to Building Cloud Native Applications) 等は、タイトルの存在は確認できたが、個別ページ URL の実地確認に至らず未収録。
- ページ取得 API のレート制限 (429) により、個別確認は上記 7 ページに留まった。
- プラットフォーム自体が引退済みのため、「無料コースとして現役」という前提は成立しない。収録 6 件はすべて「ページが現在も内容を表示すること」を確認したものだが、受講機能の存続は保証されない。

## 検証方法

1. 列挙: VMware 公式ブログと補助一覧でコース名を把握
2. URL の取得: 検索結果および補助ページに現れた kube.academy の URL をそのまま使用 (組み立て・推測なし)
3. 実在確認: 各 URL を実際に開き、タイトル・レベル・説明・アウトラインが表示されることを確認。内容が表示されなかった Containers 101 は除外した
