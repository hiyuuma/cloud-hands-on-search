# Next.js Learn / Vercel Academy 収集報告（拡充・第2波）

- 収集日: 2026-11-18
- 出力: `data/vendor-staging/nextjs_learn.json`（**31件** = Next.js Learn 4件 + Vercel Academy 27件）

## 使った公式ページ

- Next.js Learn: nextjs.org の公式 llms.txt でコース一覧を確認し、各コースページを直接開いて検証
  - App Router（/learn/dashboard-app）、React Foundations（/learn/react-foundations）、Pages Router（/learn/pages-router）、SEO（/learn/seo）
- Vercel Academy: 公式索引ページ https://vercel.com/academy（13コース掲載）および公式マシンリーダブル索引 https://vercel.com/academy/llms.txt（全コース・全レッスン掲載、全文を読了）

## 無料の切り分け方法

- Next.js Learn: 公式ページ上で「free」と明示された無料対話コースのみ（4件全て該当）。
- Vercel Academy: 全コースとも価格表示・課金導線がなく、レッスン本文は未ログインでも公開されている（進捗記録のみ無料のVercelアカウントでのサインインが必要）。有料コースは存在しないため、公式索引に載る全27コースを収録した。

## 検証方法

- Next.js Learn 4件は各コースページを実際に開いてタイトル・説明を確認。
- Vercel Academy 27件は公式 llms.txt の「Course overview」リンクからコース単位で列挙し、タイトルと説明文は同索引の公式テキストを転記した。各コースURL（/academy/<slug>）は、索引内の相対リンクを vercel.com ドメインで解決したもの。加えて主要コースは検索クロール（公式ページおよび公式 staging ミラー）でも実在を確認した（nextjs-foundations、ai-sdk、ai-summary-app-with-nextjs、slack-agents、subscription-store、building-agents-with-eve、enterprise-apps-agents、build-ai-agent-harness、build-and-launch-with-ai、ai-gateway 等）。
- 所要時間は公式に明示のある2件のみ転記（Slack Agents「~6–8 hours for the core path」、Deploy on Vercel「1-hour video series」）。レベルは公式明示がないため全件空欄（Next.js Learn の React Foundations のみページが beginner-friendly と明示するため Beginner）。

## カバレッジの限界

- vercel.com/academy のHTML索引は13コースのみをフィーチャー表示しており、llms.txt の27コースとは差がある。本収録はより網羅的な公式 llms.txt を正とした。
- Vercel Academy は新規コースの追加が頻繁（収集時点でも11月開講コースあり）。llms.txt は随時更新されるため、再収集時は同索引の差分確認が有効。
- コース内のレッスン単位では収録していない（コース単位が指定のため）。
