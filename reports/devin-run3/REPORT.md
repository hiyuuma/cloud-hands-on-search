# Run 3 報告 — 改善パッケージ I1〜I4

状態: 完了 (2026-11-18)

前提: 既存 42 テストを壊さないこと。結果は **73 passed** (既存 42 + 新規 31)。

## I1 導線100%化 — 判断根拠と結果

**結論: Google の none 22件すべてに kind=search の導線を付与でき、
none は全カタログで 0 件になった。**

根拠 (捏造せず確認できた実在パターンのみ採用):

- `data/vendor/google_skills.json` 内部に、既に **58 レコード**が
  `https://www.skills.google/catalog?locale=ja&search=<URLエンコードしたタイトル>`
  という Google Skills 公式カタログ検索 URL を持っていた。
  「元データ内に実在する URL パターン」という条件を満たすため、
  URL を持たない 22 件に同形式で kind=search を生成した。
- plan オーバーレイ側にも同じ扱いを適用した: cloud 値が分かる行で
  URL が無い場合、cloud 別の確認済みパターン (AWS: skillbuilder.aws
  search / Azure: learn.microsoft.com search / GCP: skills.google catalog)
  で kind=search を生成。cloud が分からない行は none のまま残る。
  Azure の検索パターンは `https://learn.microsoft.com/ja-jp/search/?terms=`
  が実在の公式検索ページであることを別途確認した。
- ついでの修正: 元データの `/catalog` リンク 58 件はラボ本体ではなく
  検索結果への導線なのに kind=direct に分類されていた。
  direct/search の厳密な区別 (PLAN.md) に従い kind=search に再分類した。

再生成後の実数 (vendor 893件、build/link_report):

| catalog | total | direct | search | none |
|---|---|---|---|---|
| aws | 167 | 23 | 144 | 0 |
| azure | 550 | 550 | 0 | 0 |
| google | 176 | 96 | 80 | 0 |

google は direct 96 (変更前154) / search 80 (=元データの /catalog 58件の
再分類 + 新規生成 22件)。none は全件 0 (plan フィクスチャ込み 896件の
DB でも HO-SAMPLE-002 (Azure, URL無し) に learn.microsoft.com search が
付き、HO-SAMPLE-003 は引き続き T2 で direct に格上げされる)。

## I2 検索精度

- **短クエリの単語境界マッチ**: 3文字未満の語は LIKE フォールバックで
  「前後が ASCII 英数字でない」位置にのみマッチするよう絞り込む
  (`(?<![0-9A-Za-z])term(?![0-9A-Za-z])`)。日本語文字を境界に含めないのは
  「生成AI」「音声AI」のような正当なマッチを守るため。
  `search "AI"` で "Available"/"Availability" を含むだけのレコードは
  全件除去されることをテストで検証 (test_short_query_word_boundary)。
- **検索モード**: `search(..., mode="and"|"or"|"phrase")` を API に追加し、
  CLI に `--mode` を追加 (既定 and=従来の全語一致)。FTS5 では AND/OR/フレーズ
  を MATCH 式で表現し、LIKE フォールバック側も同じ意味論を持つ。
- **ゴールデンクエリ**: 4件→15件に拡充。実データでの出現を確認済みの語のみ
  採用 (Fargate / MCP / PostgreSQL / Kubernetes / Lambda / VPC / IAM /
  Terraform / コンテナ / セキュリティ / ネットワーク / データベース /
  RAG / Cloud Run / AI)。各クエリの期待条件は tests/test_search.py の
  `GOLDEN_QUERIES` コメントに明記。parametrize で機械検証する。

実測 (build/catalog.db、各クエリ limit=5 で 1件以上ヒット):

| クエリ | ヒット | top1 |
|---|---|---|
| Fargate | 2 | Create a CI/CD pipeline ... AWS Fargate |
| MCP | 5 | Develop a speech agent with the Azure Speech MCP server |
| PostgreSQL | 5 | Explore PostgreSQL architecture |
| Kubernetes | 5 | Deploy applications to Azure Kubernetes Service |
| Lambda | 5 | Deploying an Application to AWS Lambda |
| VPC | 5 | VPC Logging and Troubleshooting |
| IAM | 5 | Cloud IAM: Qwik Start |
| Terraform | 5 | Google Cloud で Terraform を使ってみる |
| コンテナ | 5 | Deploy containers to Azure App Service |
| セキュリティ | 5 | Google Cloud で実現する信頼とセキュリティ |
| ネットワーク | 5 | Configure network security groups |
| データベース | 5 | Back up and restore databases |
| RAG | 5 | Explore Azure Storage for nonrelational data |
| Cloud Run | 5 | Hello Cloud Run [APPRUN] (Azure) |
| AI | 5 | Build Production-Ready Generative AI Applications on AWS |

mode 実測: `"Fargate PostgreSQL"` は and=0件 / or=36件。
`"Kubernetes in Google Cloud"` phrase=4件。

## I3 推薦の最適化 (ナップサック DP)

- `recommend()` の貪欲パックを `_pack_knapsack()` に置き換え。
  duration_min 判明レコードについて、合計時間 ≤ 空き時間かつ件数 ≤ limit
  の制約で**スコア合計を最大化**する 0/1 ナップサックを DP で解く。
- 決定性: 候補は従来どおり決定的ソート (score降順→所要時間昇順→id) 済みで、
  DP の更新は厳密にスコア向上時のみ。同スコアの解は合計時間が小さい方を
  採用するため同入力→同出力が保証される。出力順も従来のスコア順を維持。
- duration 不明レコードの扱い (時間にカウントせず末尾に「所要時間不明」と
  明示して追加) は現行仕様を維持。
- 効率化: 判明レコードの合計時間 ≤ 空き時間なら「全件収まる」ため
  スコア順 limit 件が最適となり DP を省略。minutes > 20000 の異常値は
  スコア順フォールバック (DP 状態数の爆発防止、レポート記載の既知の制限)。
- 検証: A(60分,score9)/B,C(30分,score6)・空き60分の入力で、貪欲は A のみ
  (合計9) を選ぶのに対し DP は B+C (合計12) を選ぶことをテストで実証。
  既存の時間上限・決定性・理由付与テストも全て通過。

## I4 正規化の残件

- **AWS plan_month**: 正規表現 `^(\d{4}-\d{2})\s+(.+)$` で
  plan_month / plan_theme に分割。実データは 157件すべて "YYYY-MM テーマ"
  形式で **全件分割できた (分割不能 0件)**。元の複合値は raw に残る。
- **Azure levels**: `level` は元の文字列 ("intermediate;advanced") を保持し
  つつ、`levels` リストを追加 ("intermediate;advanced" →
  `["intermediate","advanced"]`)。DB スキーマにも levels 列を追加
  (JSON カラム)。level 絞り込みは levels がある場合は各要素への部分一致、
  無い場合は従来どおり level 文字列の部分一致。
  実データの複数値は 2件 ("beginner;intermediate", "intermediate;advanced")、
  分割不能 0件。

## テスト結果

実行コマンド:

    .venv/bin/python -m pytest tests/ -q

結果: **73 passed** (1.5s) — Run 2 の 42 テスト + 新規 31 テスト

新規テスト内訳:
- test_etl.py (+6): google no-url→search 22件・パターン一致、/catalog 再分類、
  google none=0、plan 側同ルール適用、AWS plan_month 分割、Azure levels
- test_search.py (+6 +15 parametrized): 単語境界ノイズ除去、mode 拒否、
  OR/phrase/短フレーズ、level 複数値フィルタ、ゴールデンクエリ15件
- test_recommend.py (+3): 貪欲が最適でない入力で DP が高スコア、決定性、
  limit 制約
- test_cli.py (+1): --mode or/phrase の CLI 動作

## ETL 再生成

`PYTHONPATH=src .venv/bin/python -m hands_on_search.etl` を実行済み。
build/unified.json / link_report.{json,md} / catalog.db は上記の新しい
実数 (direct 669 / search 224 / none 0) を反映している。

## 既知の制限

- 短クエリの単語境界は ASCII 英数字ベース。「生成AI」のような日本語+ASCII
  語の連結は正しくマッチするが、「AI2」のような英数字連結語は「AI」と
  別語とみなされマッチしない (データ上は問題になっていない)。
- OR 検索で 3文字未満の語を1つでも含むクエリは全体が LIKE 経路になる
  (trigram が索引化できないため)。件数が多い語との OR は遅くなり得る。
- phrase は FTS5 フレーズマッチ (連続する文字列) であり、単語間の記号
  ゆれは吸収しない。
- knapsack DP は minutes ≤ 20000 の範囲で実行。超過時は貪欲相当の
  フォールバック (実用上の空き時間では到達しない想定)。
- level 絞り込みは要素への部分一致のため、"inter" のような部分語でも
  マッチする (従来仕様の維持)。
- plan オーバーレイで cloud が未設定の行は検索パターンを決められず
  none のまま残り得る (現フィクスチャでは全行 cloud あり)。
- Run 2 同様、CLI 実行には `PYTHONPATH=src` が必要。
