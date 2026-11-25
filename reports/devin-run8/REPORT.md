# Run 8 報告 — AI提供元/エージェント・MCP/FDE 系カタログ拡大

状態: **完了** (2026-11-26)

## 方針と制約の遵守

- Run 7 の未コミット変更 (summary_ja 22ファイル) は一切触れていない。
  reset/checkout/stash/clean・git コミットなし。
- 公式カタログの実在確認済み直行リンクのみ収録。推測 URL なし。
- staging 形式を遵守。level/duration は公式に無ければ空欄。
- access は _STAGED_ACCESS_BY_CATALOG でカタログ単位に設定。
  Free と断定できないものは unknown。

## カタログ別追加件数

| catalog | ファイル | 件数 | access | 備考 |
|---|---|---|---|---|
| openai | openai_academy.json | 14 (新規) | Free | OpenAI Academy 全14コース |
| palantir | palantir_learn.json | 26 (新規) | unknown | FDE系。要Foundryアクセスを description 明記 |
| microsoft_curricula | microsoft_curricula.json | 52 (新規) | Free | GitHub公式3カリキュラム (agents 18 + genai 21 + mcp 13) |
| deeplearning_ai | deeplearning_ai.json | 45 (新規) | unknown | エージェント/MCP/RAG/評価系を選別 |
| cohere | cohere_llmu.json | 10 (新規) | Free | LLMUモジュール→docs.cohere.com 対応付け |
| cloudflare | cloudflare_agents.json | 11 (新規) | Free | Agents SDK + MCP ガイド |
| vercel | vercel_academy.json | 10 (新規) | unknown | AI SDK/エージェント系のみ |
| anthropic | (差分なし) | 29 (変更なし) | unknown | academy.claude.com 突合・スラッグ29件完全一致 |
| huggingface | huggingface_learn.json | 12→13 | Free | Cookbook 追加 + llm-course URL更新 |
| kaggle | kaggle_learn.json | 17→18 | Free | 5-Day AI Agents Intensive 追加 |

**総件数: 2,073 → 2,243 (+170)**

## 選別基準

- deeplearning_ai: 全271コースから、エージェント構築・MCP・RAG・評価・
  ガードレール・LLMOps・コンテキストエンジニアリング等テーマ適合の45件
  (Anthropic共同制作・crewAI・LangGraph・AutoGen・Mistral 含む)。
- palantir: 公開カタログの英語コース26件を全収録 (日本語版は対象外)。
- vercel: AI/エージェント関連のみ (Next.js Learn と重複する基盤系は除外)。
- cloudflare: MCP ガイド8件 + Agents SDK ハンズオン3件。
- cohere: LLMU モジュール一覧が JS 描画で直接列挙不可のため、公式ブログの
  モジュール解説と現行 docs.cohere.com ページを対応付けて10件。

## 調査のみ (収録見送り) と理由

- **Mistral**: academy/courses の公式ドメインが存在せず独自カタログ確認できず。
  DeepLearning.AI 経由のコース (Getting Started with Mistral 等) でカバー済み。
- **Meta (ai.meta.com)**: 公式ラーニングカタログなし。
- **xAI**: 公式学習カタログなし。
- **CrewAI**: learn.crewai.com は DeepLearning.AI コースへの単発
  ランディングでカタログではない。同コースは deeplearning_ai で収録済み。
- **LlamaIndex**: llamaindex.ai/learn は404。体系立った公式アカデミーなし
  (docs のチュートリアル止まり)。

## ゴールデンクエリ実測 (build/catalog.db)

| クエリ | 結果 |
|---|---|
| FDE | palantir 24件 + openai 1件 (limit 25) |
| MCP | microsoft_curricula / cloudflare / anthropic / deeplearning_ai / huggingface 等に横断ヒット (limit 100) |
| OpenAI | openai カタログがヒット |

注: OpenAI Academy には MCP を標榜するコースが存在しないため、MCP 横断
テストは openai を除く5カタログで固定 (捏造はしない方針に基づく)。

## テスト

- `tests/test_etl.py`: カタログ別件数・総件数 (2243)・_raw_url_set・
  RUN5_CATALOGS (Run 8 の7カタログ追加)・billing (unknown 4カタログ)・
  duration 空欄件数・unconvertible (kaggle "5 days" 1件) を更新。
- `tests/test_search.py`: FDE/MCP横断/OpenAI のゴールデン3件追加。
  test_golden_mcp_livelabs は新規MCPコンテンツ増加に伴い limit 15→100。
- `tests/test_related.py`: 総件数 2076→2246。
- `tests/test_link_lang.py`: ja 合計は 660 のまま (新規カタログは全件 en リンク)。
- **結果: `.venv/bin/python -m pytest tests/ -q` → 120 passed**

## 再生成物

- build/unified.json (2,243件), build/catalog.db, build/link_report.*
- web/unified-compact.json (2,243件・従来と同一15キー構成)
- README のカタログ表 (計38ソース) 更新
- reports/catalog-expansion/ に新規7件 + 更新記録1件を追加

## 既知の制限

- cohere は LLMU モジュール名と docs 現行ページの対応付けであり、
  LLMU 本来のモジュールURL (JS描画) は取得できていない。
- deeplearning_ai の level/level 表記・priority はカタログデータ由来。
- palantir/vercel/deeplearning_ai は access=unknown (料金断定不可)。
- summary_ja の yomiyasu 最終チェックは未実施 (新規分は方針に沿って簡潔に記述)。
