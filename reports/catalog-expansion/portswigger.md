# PortSwigger Web Security Academy 収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/portswigger.json` (**31件**)

## 使った公式ページ

| ページ | URL | 用途 |
|---|---|---|
| Web Security Academy トップ | https://portswigger.net/web-security | Academy 全体が無料であることの確認 |
| All labs | https://portswigger.net/web-security/all-labs | トピック見出し31件の母集団列挙 |
| 各トピックページ (31件) | portswigger.net/web-security 配下 (JSON の url 参照) | トピック名・説明文・URL の実在確認 |

## 件数と内訳

- 収録件数: **31件** (全件 type = `topic`。トピック単位の教材+ラボ群として収録し、個別ラボ (約274件) は対象外)
- priority 内訳: 高26件 / 中5件 (Essential skills、Prototype pollution、Race conditions、Web LLM attacks、Web cache deception)。全件が Web セキュリティ実践のため原則「高」、発展・ニッチ領域を「中」とした
- domain: 全件 `セキュリティ・IAM` / services: 全件 `Burp Suite`
- level: 全件 null。Academy はトピック単位のレベルを持たず、ラボ単位で Apprentice / Practitioner / Expert の3段階があるため、トピックに単一レベルを推測で付けなかった
- duration_text: 全件 null (公式にトピック単位の所要時間は公開されていない)
- description: 16件は公式トピックページ冒頭の説明文を転記、15件は冒頭文が取得できなかったため空 (推測で書いていない)

## 無料の切り分け方法

Web Security Academy は教材・ラボとも **全編無料** (公式トップページおよび各種公式案内で確認。無料アカウント登録で進捗管理が可能)。有料なのは Burp Suite Professional 本体と BSCP 認定試験であり、Academy の教材自体に対象外となる有料コンテンツはない。そのため31トピック全件を収録した。

## 検証方法

1. 母集団: 公式 All labs ページ (2026-11-18 取得) のトピック見出し31件を列挙。第三者の網羅マップ (2026-08-20 に公式 all-topics を読んだ記録) でも31トピックで一致
2. URL 実在確認: 31件すべてについて、検索結果に返された公式 URL (Full URLs) または公式の子ページ (ラボ/下位セクション) の URL から親トピックのパスを実在確認した。**URL の推測・組み立てはしていない**。実際、推測と異なるスラッグが複数あった:
   - Path traversal → `file-path-traversal`
   - OS command injection → `os-command-injection`
   - Business logic vulnerabilities → `logic-flaws`
   - Insecure deserialization → `deserialization`
   - Web cache poisoning → `web-cache-poisoning`
   - Web cache deception → `web-cache-deception`
   - Web LLM attacks → `llm-attacks`
3. Race conditions のみ、検索で返る URL がトラッキング用クエリ付き (`?source=post_page-----…`) だったため、クエリなしの正規パスで収録した (パス部分自体は返却 URL で一字一句確認済み)

## カバレッジの限界

- 個別ラボ単位 (約274件、第三者集計では Apprentice 61 / Practitioner 174 / Expert 39) では収集していない。トピック→ラボの二層化が必要なら、ライブブラウザでの追加収集が別途必要
- ラボ数は変動する (2026-04 に Web LLM attacks へ AI-powered scanner 系ラボが追加され総数が増えた経緯あり)。本収集の31トピックは 2026-11-18 時点の構成
- description が空の15件は、統合側で必要なら各トピックページ冒頭文を後追い取得できる
