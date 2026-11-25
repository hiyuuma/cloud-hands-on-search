# DEVIN RUN 8 指示書 — AI提供元／エージェント・MCP／FDE 系カタログの拡大追加

あなたは Devin CLI (SWE-2 medium) として、このワークスペースで作業する自律実装担当です。
Run 1〜7 の報告 (reports/devin-run1〜7/REPORT.md) と docs/LEDGER.md をまず読んでください。
既存テストを壊さないことが前提です。

## 最重要の注意 (作業ツリーの状態)

- ワークツリーには **Run 7 (summary_ja 拡充) の未コミット変更が22ファイル分残っています**。
  これは司令塔がまだ検収していない別作業です。**絶対に reset / checkout / stash /
  clean をしないこと**。既存ファイルへの変更は「追記・差分追加」のみとし、
  Run 7 が書き直した summary_ja を元に戻したり上書きしたりしないこと。
- git コミットはしない (司令塔が検収してからコミットする)。進捗の節目ごとに
  reports/devin-run8/REPORT.md を更新して、中断しても再開できる形にすること。

## 目的

ユーザー指示「AnthropicやOpenAIなどが提供しているコース (FDE、MCP のような領域)
も調べて追加して。対象は広めに」で承認された拡大版です。現在の 31ソース・2,073件に、
AIモデル提供元／エージェント・MCP特化／FDE・導入支援系の公式カタログを追加します。

## 収録ルール (従来どおり厳守)

- **公式カタログのみ**。URL は実際に公式ページを開いて実在を確認した直行リンクのみ。
  推測で URL を組み立てない。確認できないコースは収録せず REPORT に理由を書く。
- 各レコードは既存 staging 形式 (title / url / type / level / duration_text /
  description / domain / services / priority_for_user / summary_ja) で書く。
  description は公式文面ベース、summary_ja は Run 7 基準 (2〜3文・80〜180字目安、
  体言止め・常体、元データの範囲のみ、捏造禁止)。
- level や duration が公式に無い場合は推測で埋めず空欄にする。
- access (無料/有料) はカタログごとに実態を確認して loaders.py の
  _STAGED_ACCESS_BY_CATALOG に正しく設定する。断定できないものは "unknown"。
  特に DeepLearning.AI は無料と断定しないこと。
- 日本語の読み物として summary_ja は yomiyasu スキルが使えれば最終チェックに使う。

## 追加対象 (司令塔が 2026-11-26 に公式ソースで実在確認済み)

### 新規カタログ

1. **openai (OpenAI Academy)** — 最優先・現在ゼロ件。
   母集団: OpenAI Help Center のコース一覧
   https://help.openai.com/en/articles/20001270-openai-academy-courses
   (AI Foundations / Applied AI Foundations / Agents and Workflows / Scope AI
   Solutions / Evaluate AI Applications / Design and Build Agentic Systems /
   Build with RAG / Optimize AI Application Performance / Get Started with
   Codex / Extend Codex Workflows / Scale Codex / AI Leadership / AI for
   Educators / AI for College Students 等、表に載る全コース) と
   https://academy.openai.com/pages/courses の実在ページで裏取りする。
2. **palantir (Palantir Learn)** — FDE の本家。https://learn.palantir.com/ の
   コース一覧から、Foundry & AIP Aware、AI Engineer トラック、Speedrun 系、
   Deep Dive 系、Scoping Use Cases、Applied Notional Project 等を収録する
   (全件ではなく主要コース 20〜40件程度に選別し、選別基準を REPORT に書く)。
   多くのコースは Foundry アクセスが前提 — その旨を description に明記する。
3. **microsoft_curricula (Microsoft 公式 GitHub カリキュラム)** — Azure Learn とは別枠。
   - https://github.com/microsoft/mcp-for-beginners (モジュール単位で収録)
   - https://github.com/microsoft/ai-agents-for-beginners (レッスン単位で収録)
   - https://github.com/microsoft/generative-ai-for-beginners (レッスン単位で収録)
   各レッスン/モジュールの直行リンク (GitHub 内の該当フォルダ/ファイル) を使う。
4. **deeplearning_ai (DeepLearning.AI 短編コース)** —
   https://www.deeplearning.ai/courses から、エージェント／MCP／RAG／評価／
   コンテキストエンジニアリング等のテーマに合う短編コースを選別収録する
   (目安 25〜45件、選別基準を REPORT に明記。全件収録はしない)。
   Anthropic 共同制作 (MCP、Agent Skills、Claude Code 等) や crewAI、
   LangGraph、LlamaIndex、AutoGen、Mistral のコースもここに含まれる。
5. **cohere (Cohere LLM University)** — https://docs.cohere.com/docs/llmu-2 を
   起点にモジュール単位で収録 (LLM基礎、Text Representation、Text Generation、
   RAG、Tool Use、Deployment、Semantic Search、Prompt Engineering 等)。
6. **cloudflare (Cloudflare Agents / MCP ガイド)** —
   https://developers.cloudflare.com/agents/model-context-protocol/guides/ 等の
   公式ガイド・ラーニングパスから、エージェント／MCP テーマのものだけを
   「guide」種別で選別収録する (目安 8〜15件)。
7. **vercel (Vercel Academy)** — https://vercel.com/academy の AI SDK コース、
   Slack Agents 等のコース単位で収録 (目安 4〜10件)。Next.js Learn (既存
   nextjs カタログ) と重複するものは入れない。

### 既存カタログの拡充 (追記のみ)

8. **anthropic** — https://academy.claude.com/ の現行コース総数と既存29件を
   突合し、新規コースがあれば追記する。差分が無ければ REPORT に「差分なし」と
   明記する (無理に追加しない)。
9. **huggingface** — 既存12件に未収録なら次を追記する: Agents Course
   (https://huggingface.co/learn/agents-course)、MCP Course、Context Course、
   LLM Course 等、Learn 配下の主要コース。
10. **kaggle** — 未収録なら「5-Day AI Agents Intensive Course with Google」
    (https://www.kaggle.com/learn-guide/5-day-agents) を 1件 (または Day 単位で
    リンクが実在すれば最大5件) 追記する。

### 調査のみ (収録しない可能性が高いもの)

11. **Mistral AI / Meta / xAI** — 独自の公式コースカタログが実在するか確認し、
    無ければ「公式カタログなし」と REPORT に書く。第三者サイト (まとめサイト、
    非公式アカデミー) のコースは絶対に収録しない。Mistral は DeepLearning.AI
    経由のコースでカバーされる旨を書く。
12. **CrewAI / LlamaIndex の独自アカデミー** — 公式の体系立ったコースが実在
    すれば小規模に収録可。ドキュメントのチュートリアル止まりなら収録せず
    REPORT に判断を書く。

## FDE の扱い

- 統一スキーマに tags フィールドは無いため、新フィールドは追加しない。
- Palantir のコースは domain を「AIエージェント・FDE」等の検索に掛かる値にし、
  summary_ja には (内容が許す範囲で) FDE (Forward Deployed Engineer) /
  顧客導入・ユースケーススコーピングといった語を自然に入れる。
- OpenAI の Scope AI Solutions、Anthropic の導入系コース等、導入支援に直結する
  既存・新規レコードも同様に、summary_ja に FDE 的文脈を無理のない範囲で含める。
- ゴールデンクエリ: 検索 "FDE" で Palantir を中心に複数件ヒットすること、
  "MCP" で openai/anthropic/microsoft_curricula/huggingface/deeplearning_ai/
  cloudflare を横断してヒットすること、"OpenAI" で openai カタログが
  ヒットすることをテストで固定する。

## 実装

- etl.py の RUN5_CATALOG_FILES に相当する仕組みに新規カタログを登録する
  (命名は既存の流儀に合わせる)。loaders.py の staged 経路をそのまま使う。
- テストの総件数固定 (現在 2,073件) は新しい総件数に更新し、カタログ別の
  件数テストも追加する。link_lang テストの ja 合計 (660) は新規分で変わる
  場合は実測に合わせて更新し、根拠を REPORT に書く。
- ETL を再生成する: build/unified.json、build/catalog.db、
  web/unified-compact.json (従来と同じフィールド構成で)。
- README のカタログ表を更新する。

## 成果物

- data/vendor/ の新規・追記 JSON、etl/loaders の登録、テスト更新、ETL 再生成物
- reports/catalog-expansion/ に新規カタログごとの収集報告 (従来形式:
  使った公式ページ、件数と内訳、検証方法、カバレッジの限界)
- reports/devin-run8/REPORT.md: カタログ別追加件数、総件数の変化、
  ゴールデンクエリ実測、調査のみで見送った提供元と理由、既知の制限

## 制約

- Python 3.12 標準ライブラリのみ (テスト用 pytest は可)。pip 追加禁止
- テストは `.venv/bin/python -m pytest tests/ -q` で全件通ること
- 課金が発生する操作はしない。ログインが必要なページの先は追わない
  (公開カタログ情報の範囲で収録する)
