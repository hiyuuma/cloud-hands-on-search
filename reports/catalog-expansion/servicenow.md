# ServiceNow (ServiceNow University / Now Learning) 収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/servicenow.json` (**20件**: course 18件 / learning-path 2件)

## 使った公式ページ

- ServiceNow University (旧 Now Learning): https://learning.servicenow.com/lxp/en/pages/servicenow (トップは Cookie バナー+JS シェルのみ取得可)
- 検索インデックスに載った learning.servicenow.com / nowlearning.servicenow.com のコースページ本文 (About this Course、対象リリース、所要時間)
- ServiceNow 公式コミュニティ (servicenow.com/community) の投稿に引用されたコース URL と、公式 FAQ スレッド「[ServiceNow University] - Vouchers eligibility, Free Trainings, Paid Exams and Payments」

## 無料の根拠

- 公式 FAQ 系スレッドで「全てのオンデマンドコースは無料 (トレーニングは無料、認定試験バウチャーは有料)」と繰り返し案内されている
- Enterprise Architecture (EA) Fundamentals の前提条件欄でも Welcome to ServiceNow が "quick, free" と明記されている
- そのため本収集は「オンデマンドコース/学習パス」に限定し、講師主導 (ILT) のみの教材や試験そのものは対象外とした

## 件数と充足率

- duration_text 充足: 2/20件 (TSOM Bootcamp "7 hours 10 minutes"、Discovery Basics for SAM "2 hours 55 minutes" — コースページの表示原文)
- level: 出典に明示がほぼ無く全件空欄 (推測で埋めていない)
- description: 16/20件に公式の About 本文を設定。モバイル系3件はコミュニティ投稿で存在とタイトルのみ確認できたため簡潔な注記に留めた

## カバレッジの限界 (正直な報告)

- LXP のコースページは JS アプリで、テキスト取得ではタイムアウトし直接開いての全文確認ができなかった。検証は「検索インデックスに保持された公式ページ本文」と「公式コミュニティ投稿での引用」の突合による
- 母数 (オンデマンドコース数百件規模) に対し20件はごく一部。上限100件に届いていない。特に Scripting in ServiceNow Fundamentals、Application Development Fundamentals、ITSM Fundamentals 本体など主要コースは、コミュニティ投稿内で URL が途中で省略表示され完全な URL を確認できなかったため、制約を優先して除外した
- 13件は検索結果に提示された完全な URL (course_id 付き) をそのまま転記。7件 (Welcome to ServiceNow 等) は公式コミュニティ投稿本文に完全なパスまで表示されていた URL を、省略されていたクエリ文字列なしで転記した
- nowlearninguat.service-now.com (UAT環境) にインデックスされていたコース (AI Agents Essentials 等) は、本番 URL を推測で作らないため収録していない

## 検証方法

1. learning.servicenow.com / nowlearning.servicenow.com ドメインのコースページが検索インデックスに保持した本文で、タイトルと About 内容の対応を確認
2. 無料であることは公式 FAQ スレッドとコースページ内の "free" 明記で確認
3. URL の推測・組み立て・UAT→本番のホスト置換は一切していない
