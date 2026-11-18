# Neo4j GraphAcademy 収集レポート（第2波）

- 収集日: 2026-11-18
- 出力: `data/vendor-staging/neo4j_graphacademy.json`
- 総件数: **60件**（course 46件 / workshop 14件。全件無料・セルフペース）

## 使った公式ページ

- 公式コース索引: https://graphacademy.neo4j.com/llms.txt （全コースのスラッグとタイトルを列挙した公式インデックス）
- カテゴリページ群: `/categories/beginners`、`/categories/cypher`、`/categories/development`、`/categories/generative-ai`、`/categories/aura`、`/categories/processing`（基礎）、`/categories/foundation`、`/categories/workshops`（所要時間と説明文の出典）
- 個別コース概要（llms.txt 形式）: administration-docker-cluster、administration-role-based-access、aga-centrality、gds-shortest-paths（カテゴリページで不足した分の補完）

## 検証方法

1. 列挙の母集団は公式 llms.txt 索引の全60コース。漏れ・重複なし（JSON検証で重複0を確認）。
2. コースURLは `https://graphacademy.neo4j.com/courses/<slug>` 形式。形式自体は GitHub 公式組織ページとカテゴリページのアウトリンクで原文確認済みで、スラッグはすべて llms.txt 由来（推測スラッグなし）。
3. duration_text と description はカテゴリページの表示原文を記録。出典にないものは空欄にした: 所要時間なし3件（Understand centrality algorithms、Role-Based Access Control in Neo4j、Workshop de Neo4j e IA Generativa）、説明文なし1件（同ポルトガル語GenAIワークショップ）。
4. level は公式の Beginners カテゴリに属する12件のみ "Beginner" を記録し、他は空欄（コース単位のレベル表記が公式にないため）。

## 収録内容の内訳

- 基礎・Cypher・モデリング・インポート: Neo4j Fundamentals、Cypher Fundamentals ほか約20件
- 開発（ドライバ/アプリ）: Python / Java / Go / .NET / TypeScript / Spring Data / GraphQL の7件
- Aura・運用: AuraDB Fundamentals、Aura In Production、Docker運用ラボ、RBACラボほか
- グラフデータサイエンス: GDS Fundamentals、Path Finding、中心性ラボ、Aura Graph Analytics ほか
- GenAI / MCP / エージェントメモリ: GraphRAG（Python/TypeScript）、Neo4j MCP Server、FastMCP、LangChain、Agent Memory 系ワークショップなどAIドメイン15件
- ポルトガル語ワークショップ5件（priority「低」で収録）

## カバレッジの限界

- llms.txt 索引が公式の全コース列挙である前提に立つ。索引自体に載らない限定公開コース等があれば拾えない。
- 認定試験（Neo4j Certified Professional 等）はコースではないため対象外。
- ワークショップ系は元々講師開催用教材だが、GraphAcademy 上で無料セルフペース公開されているため収録した（type="workshop" で区別）。
