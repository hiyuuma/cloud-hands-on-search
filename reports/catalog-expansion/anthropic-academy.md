# Anthropic Academy 収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/anthropic_academy.json` (**23件**)

## 使った公式ページ

| ページ | URL | 用途 |
|---|---|---|
| Anthropic Courses (Skilljar カタログ トップ) | https://anthropic.skilljar.com/ | コース一覧の母集団 (2026-11-18 取得時点で23項目を確認) |
| 各コース詳細ページ (22件) | anthropic.skilljar.com 配下 (JSON の url 参照) | タイトル・説明文の実在確認 |
| AI Fluency for pK-12 Educators (ラーニングパス) | https://anthropic.skilljar.com/path/ai-fluency-for-pk-12-educators | パスの実在確認 |
| Claude Academy (新公式サイト) | https://academy.claude.com/ | 所要時間の裏取り (下記参照) |

補助的に、Skilljar カタログへのリンク集を持つ第三者ガイド (DevtoolHub の Anthropic Academy 全22コース解説、2026-11-11 に公式サイトで検証済みと明記) から各コースページへ辿り、公式ページ側でタイトルと内容を確認した。URL はすべて公式ページを開いて実在を確認したもので、推測・組み立てはしていない (実際、Building with the Claude API の URL は `claude-with-the-anthropic-api`、Claude with Amazon Bedrock は `claude-in-amazon-bedrock`、Claude on Google Cloud は `claude-with-google-vertex` と、タイトルからの推測とは異なるスラッグだった)。

## 件数と内訳

- 収録件数: **23件** (course 22件 / learning-path 1件)
- 無料/有料: **全件無料**。Skilljar 上のコースはメール登録のみで受講でき、修了証も無料 (各コースページの FAQ でも「Anthropic アカウント不要・Skilljar アカウントのみでアクセス可」と明記)。有料として対象外にしたもの: Claude Certified Architect, Foundations (CCA-F) の監督付き認定試験 (受験料 $99 とされる) — これは Skilljar のコースではなく別プログラムの試験のため未収録 (1件)。
- priority 内訳: 高9件 (Claude Code 101 / Claude Code in Action / Claude Platform 101 / Building with the Claude API / Introduction to Model Context Protocol / Model Context Protocol: Advanced Topics / Introduction to agent skills / Introduction to subagents / Claude with Amazon Bedrock)、中7件、低7件 (AI Fluency の教育・非営利・クリエイティブ系など周辺領域)
- duration_text 充足: 23/23件 (ただし出典は下記の留保あり)
- level 充足: 0/23件 (公式 Skilljar ページにレベル表記がないため、推測で埋めず全件 null)

## 所要時間 (duration_text) の出典について

Skilljar のコースページには所要時間が表示されない。duration_text は、後継の公式サイト academy.claude.com のコース一覧に掲載された Length を転記した第三者ガイド (Coursiv、2026-10-22 に公式サイトで検証) の値を採用し、別の独立ガイド (Sandlabs、2026-10-31 検証) の値と突合して一致を確認した。さらに AI Capabilities and Limitations の「3.5 hr」は、こちらで academy.claude.com トップを取得した際にも直接確認できた。pK-12 のパスは academy 側で2コース (3 hr + 45 min) に分かれているため、その合算表記にした。

## 検証方法

1. 母集団の列挙: 公式 Skilljar カタログトップ (当日取得) に載る全23項目を列挙
2. 実在確認: 23件すべてについて公式コース/パスページを実際に開き、ページタイトルが公式表記と一致すること、説明文が取得できることを確認
3. 説明文: 各ページの "Additional Details" の Description、無い場合はカタログトップの説明文を採用 (いずれも公式文面)
4. 無料確認: コースページ FAQ と複数ガイドの記述で全件無料を確認

## カバレッジの限界 (重要)

- **Skilljar は 2026年12月上旬で終了予定**。一部コースページに「This legacy learning experience will no longer be available in early December 2026. Sign in at academy.claude.com to continue learning」という公式バナーを確認した。後継は **Claude Academy (academy.claude.com、2026-08-20 開設)** で、そちらは27〜28コースを掲載し、Skilljar に無いコース (Introduction to Claude Tag、The AI-native SDLC playbook、Building effective human-agent teams (beta)、AI Fluency for pK-12 Train the Trainer の単独コース等) も含む。本収集は指示どおり Skilljar カタログを正としたため、**academy.claude.com 限定コースは未収録**。URL の寿命も短い可能性があり、統合後は academy.claude.com 側 URL への差し替えを検討すべき。
- academy.claude.com は JavaScript 描画のためテキスト取得ではカタログ全件を列挙できず、今回は母集団として使えなかった (ブラウザ操作での追加収集が別途必要)。
- Coursera 上の AI Fluency 5コース (2026-05-28 開講、無料) は別プラットフォームのため対象外とした。内容は Academy 側と重複する。
- level は公式に公開フィールドが確認できなかったため全件 null。第三者ガイドのレベル付けは主観ラベルのため採用しなかった。

## 追補 (2026-11-18、ブラウザ追加収集 — Claude Academy へ切替)

後継プラットフォーム Claude Academy (academy.claude.com) を実ブラウザで収集し、カタログ表示の総数29件と一致する全29コースを詳細ページで確認した (所要時間は全件取得、レベル表示は同サイトに存在しないため空欄。料金表示自体がないため「無料」とは断定せず、各レコードの description に「料金表示なし」と前提条件を明記した)。Skilljar は2026年12月上旬に終了予定のため、anthropic_academy.json の中身は Claude Academy の29件に置き換えた (Skilljar 23件の記録は本報告の本文と git 履歴に残る)。日本語版カタログの公式タイトルを採用し、duration_text は他カタログと揃えるため "3h 30m" 形式に正規化した。分類 (domain/services/priority/summary_ja) は司令塔 (Muse) が付与した。
