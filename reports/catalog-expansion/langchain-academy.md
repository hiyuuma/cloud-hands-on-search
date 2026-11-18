# LangChain Academy カタログ収集報告

収集日: 2026-11-18 / 収集担当: Muse (サブエージェント)
出力: `data/vendor-staging/langchain_academy.json` — **18件**

## 使った公式ページ

- 全製品一覧 (All Products): https://academy.langchain.com/collections (page=1〜4 を全件取得。計19製品)
- LCAE バンドルページ: https://academy.langchain.com/bundles/lcae-prerequisite-courses (構成コースの Free 表記を確認)
- 各コースページ (全18件を個別に開き、タイトル・「About this course」の Free 表記・レッスン数・動画時間を確認)

## 件数と内訳

- 全製品 19件 = コース 18件 (収録) + バンドル 1件 (除外)
- 収録18件は **全件 Free** (各コースページの "About this course: Free" で個別確認。LCAE Practice Exam も無料だった)
- priority_for_user: 高 7件 (LangGraph / LangChain 本体・Quickstart Python・Deep Agents・Managed Agents・Ambient Agents) / 中 9件 / 低 2件 (Fleet、Practice Exam)
- level: 全件 null — 公式コースページ・一覧のいずれにもレベル表記がなかったため推測で埋めていない
- duration_text: 動画時間が 0 でない 11件に "X hours of video content" を転記。プラットフォームが "0 hours of video content" と表示する 7件は実質の所要時間として意味を持たないため "" とし、レッスン数を description 末尾に併記した

## 除外したもの

- **LCAE Prerequisite Courses Bundle** (https://academy.langchain.com/bundles/lcae-prerequisite-courses) — コースではなくバンドル (詰め合わせ) のため対象外。構成する6コース (Introduction to LangChain - Python / Introduction to Deep Agents / Building Reliable Agents with LangSmith / Building and Deploying Managed Agents / Introduction to LangSmith Agent Server / Monitoring Production Agents) は全件個別に収録済み
- LangChain Certified Agent Engineer の認定試験そのものは有料で、Academy のコース製品としては掲載されていない (掲載は無料の模擬試験のみ)

## 検証方法

- URL は全件、一覧ページのリンクを辿って開いたコースページの実 URL そのもの。推測で組み立てた URL は無い
- "Introduction to Agent Observability & Evaluations" のみ一覧ページ (page=4) でリンクが抽出できなかったため、公式ドメイン内の検索結果から URL (`/courses/intro-to-langsmith`) を特定し、実際に開いてタイトルと Free 表記を確認した
- タイトルは All Products 一覧の公式表記を採用した (コースページ側の SEO タイトルとは異なる場合がある。例: 一覧 "Introduction to LangSmith Agent Server" ↔ ページ見出し "LangSmith Agent Server: Deploy your agents to the cloud"、URL は /courses/langsmith-deployment)
- 価格は各コースページの "About this course" 欄で個別に確認した (一覧ページには価格表示がない)

## カバレッジの限界

- All Products のページングは page=4 (1件) で終端を確認した。カテゴリ別コレクション (/collections/build 等) は同じ製品の絞り込み表示であり、新規製品はなかった
- コースの新設・改称が頻繁なプラットフォームであり、本収集は 2026-11-18 時点のスナップショット
- duration はプラットフォーム申告の「動画時間」基準で、演習・実習時間を含まない。Introduction to LangGraph - Python は外部資料で「約6時間・55レッスン」と紹介される値と公式表記が一致した
