# Run 5 報告 — 第2波24カタログの統合

状態: 完了 (2026-11-18)

前提: 既存 84 テストを壊さないこと。結果は **96 passed** (既存 84 + 新規 12)。
vendor 総件数は 1,582 → **2,073 件** (+491、指示書どおり)。

## 統合サマリ

`data/vendor-staging/` の検証済み 24 ファイルを `data/vendor/` へ移動し、
Run 4 と同じ staging 形式 (`_normalize_staged`) で統合した。ローダは
24 個別関数ではなく `load_staged(path, catalog)` / `normalize_staged` 1本の
汎用実装とし、`etl.RUN5_CATALOG_FILES` (catalog キー→ファイル名) で
カタログを宣言的に追加する構成にした。billing の例外は
`loaders._STAGED_ACCESS_BY_CATALOG` でカタログ別に上書きする。

- ID: カタログ接頭辞つき (`alibaba:` 〜 `snowflake:`)。全24カタログで
  タイトルの重複が無いことを実データで確認済みのため、Run 4 と同じ
  タイトル・スラッグ方式 (hashicorp 式の URL パス ID は不要だった)。
  一意性は `test_run5_id_prefix_and_uniqueness` で固定。
- cloud: 全24カタログとも 3クラウド外のため「その他」に統一 (raw に出典を残す)。
- level: 出典の表記をそのまま保持、空欄は推測しない。
- type: 統一スキーマに該当フィールドが無いため raw にのみ保持
  (course / learning-path / certification / topic 等の区別は失われない)。

## カタログ別 統合件数と充足率

| catalog | total | duration 充足 | level 充足 | access |
|---|---|---|---|---|
| alibaba | 13 | 0/13 | 0/13 | Free 13 |
| anthropic | 29 | 29/29 | 0/29 | unknown 29 |
| cisco | 23 | 23/23 | 23/23 | Free 23 |
| confluent | 27 | 5/27 | 0/27 | Free 27 |
| databricks | 51 | 51/51 | 0/51 | Free 51 |
| datadog | 25 | 9/25 | 9/25 | Free 25 |
| elastic | 7 | 0/7 | 1/7 | Free 7 |
| fortinet | 13 | 3/13 | 1/13 | Free 13 |
| freecodecamp | 12 | 7/12 | 4/12 | Free 12 |
| huggingface | 12 | 8/12 | 3/12 | Free 12 |
| ibm | 4 | 0/4 | 4/4 | Free 4 |
| kaggle | 17 | 15/17 | 0/17 | Free 17 |
| langchain | 18 | 11/18 | 0/18 | Free 18 |
| mongodb | 21 | 21/21 | 0/21 | Free 21 |
| neo4j | 60 | 57/60 | 12/60 | Free 60 |
| nextjs | 31 | 2/31 | 1/31 | Free 31 |
| nvidia | 11 | 11/11 | 9/11 | Free 11 |
| portswigger | 31 | 0/31 | 0/31 | Free 31 |
| redhat | 12 | 5/12 | 0/12 | Free 12 |
| redis | 4 | 0/4 | 0/4 | Free 4 |
| salesforce | 22 | 17/22 | 15/22 | Free 22 |
| sap | 17 | 0/17 | 1/17 | Free 17 |
| servicenow | 20 | 2/20 | 0/20 | Free 20 |
| snowflake | 11 | 6/11 | 0/11 | Free 11 |

新規計 491 件。duration 充足 283/491 (58%)、level 充足 85/491 (17%)。

## duration 変換

`parse_duration_minutes` に1点だけ拡張を加えた: `"1,800 hours"` のような
桁区切りカンマを前処理で除去する (`(?<=\d),(?=\d{3}\b)` → 削除)。
既存のトークン抽出で以下の新表記もそのまま変換できた:

- `"14 hours"` / `"18 hours"` / `"45m"` / `"55m"` / `"1h"` (指示書の例)
- `"3 hrs and 40 mins"` / `"~7 hrs 20 mins"` (redhat / salesforce の ~ 接頭辞)
- `"1 hour 30 min"` / `"1.5 hours"` / `"7.75 Hours"` (小数・大文字ゆれ)
- レンジ・推奨ペース表記は従来どおり上限値を採用:
  `"2-3 hours"`→180、`"approximately 6-8 hours of work per week"`→480、
  `"Most learners take between 8 and 12 hours to complete this course."`→720
- 修飾語つき: `"Around 300 hours (estimated)"`→18000、
  `"1.5 hours to complete"`→90、`"6 hours of video content"`→360

**変換できなかった件数: 0 件** (非空の duration_text は全件分に変換できた。
`test_run5_duration_coverage` で固定)。
これとは別に duration_text 自体が空欄のものは 208/491 件で、
いずれも duration_min=None (推測で埋めていない)。空欄内訳:
alibaba 13 / confluent 22 / datadog 16 / elastic 7 / fortinet 10 /
freecodecamp 5 / huggingface 4 / ibm 4 / kaggle 2 / langchain 7 /
neo4j 3 / nextjs 29 / portswigger 31 / redhat 7 / redis 4 /
salesforce 5 / sap 17 / servicenow 18 / snowflake 5。

## billing (access) 判断の根拠

- **原則 Free**: 収集段階で無料確認済みのものだけが収録されているため。
- **anthropic → unknown (29件)**: 指示書どおり Free にしていない。
  収集報告 (reports/catalog-expansion/anthropic-academy.md) によると、
  JSON の中身は後継サイト Claude Academy (academy.claude.com) の29件で、
  同サイトには料金表示自体が存在しない。開始ボタン等にも課金表示は無く、
  実質無料と見られるが「無料」と断定できる根拠が無いため、既存語彙の
  「不明・要確認」に相当する `unknown` とした (LF 空欄と同じ扱い)。
- **redhat → Free (12件)**: 教材自体は無料だが、収集報告にあるとおり
  一部パスは実習に Developer Sandbox / 無償トライアル登録が必要。
  access は Free のままとし、登録が必要な点はこの既知の制限として明記する。
- **elastic → Free (7件)**: うち3件 (Data types and mappings /
  Security Quick Start / Getting started: Actions and escalate) は
  収集報告で「無料確認度が一段低い」とされたもの (無料セクション側の
  タブを展開確認できず、同一形式のオンデマンドモジュールと判断して収録)。
  統合は行ったが、この点を制限として明記する。

## 導線 (link) 内訳

staging の URL は全件 kind=direct (実在確認済み)。ETL 再生成後の
link_report 実数 (vendor 2,073 件): direct 1,849 / search 224 / none 0。
新規24カタログは全カタログで direct=total (上表の link_report を参照)。
「direct は元データに実在するものだけ」の機械テスト
(`test_no_fabricated_direct_urls`) の元データ集合に新24ファイルを追加し、
新カタログ由来の direct も同じ検査にかけている。

## 横断リンク (T2)

既存ルール (正規化タイトル一致 / URL 一致) を新カタログにもそのまま適用。
新カタログを含む新規ペアは **0 組** (全体で related 付きレコード 4件・
2組のまま、Run 4 の github_skills↔azure の2組のみ)。link 格上げも 0 件。
無理に増やしていない。

## ゴールデンクエリ実測 (build/catalog.db)

| クエリ | 条件 | 実測 |
|---|---|---|
| LangGraph | LangChain Academy がヒット | 合格: 6件ヒット、top1〜3 とも langchain (例: "Introduction to LangGraph - Python") |
| SQL injection | PortSwigger がヒット | 合格: top1 "SQL injection"、top2 "NoSQL injection" (ともに portswigger) |
| Kubernetes | Red Hat のパスがヒット | 合格: 50件中31位に "Learn Kubernetes using the Developer Sandbox" (redhat)。HashiCorp/LF 等が上位を占めるため順位は低め |
| FortiAuthenticator | Fortinet がヒット | 合格: 1件ヒット、top1 "FortiAuthenticator 8.0 Administrator" |
| Next.js | Next.js Learn がヒット | 合格: 12件ヒット、top1〜2 は nextjs ("Build with Next.js" 等) |

いずれも `tests/test_search.py` の新規ゴールデンテストとして機械検証。

## テスト

実行コマンド:

    .venv/bin/python -m pytest tests/ -q

結果: **96 passed** — Run 4 の 84 件 + 新規 12 件

新規テスト内訳:
- test_etl.py (+6): run5全件 direct、ID接頭辞と全体一意性、
  共通フィールドの raw 一致、duration 代表変換、billing
  (anthropic=unknown / 他=Free)、変換不能0件と空欄件数の固定
- test_normalize.py (+1): Run 5 の duration 表記の単体変換
- test_search.py (+5): LangGraph / SQL injection / Kubernetes(redhat) /
  FortiAuthenticator / Next.js の新ゴールデンクエリ

既存テストの更新 (件数の変更のみ、仕様の緩和なし):
- test_vendor_counts: 1,582 → 2,073 (24カタログ追加)
- test_no_merge_and_raw_preserved: 1,585 → 2,076
- _raw_url_set: 新24ファイルの url を元データ集合に追加

## ETL 再生成

`PYTHONPATH=src .venv/bin/python -m hands_on_search.etl` 実行済み。
build/unified.json (2,073 件) / link_report.{json,md} / catalog.db を更新し、
web/unified-compact.json も同じフィールド構成 (14キー) で 2,073 件に
再生成した (従来どおり unified.json からの射影)。

## 既知の制限

- duration_min は「表記された所要時間」の分換算。レンジ・推奨ペース表記
  ("6-8 hours per week" 等) は上限値を採用しており、1週あたりの量を
  総所要時間として格納している点に注意 (huggingface 等)。原文は
  raw.duration_text に残る。
- anthropic の29件は access=unknown で、access 絞り込みで「無料のみ」に
  すると出ない。Skilljar 版の収集報告では無料確認済みだったが、中身は
  後継 Claude Academy のものに置き換わっており、同サイトは料金表示自体が
  無い。課金が始まった場合に気付けるよう unknown に留めた。
- elastic の3件は無料確認度が一段低い (上記)。
- redhat の一部パスは実習に Developer Sandbox / 無償トライアル登録が必要。
- duration_text 空欄が多いカタログ (portswigger 全件、sap 全件、
  nextjs 29/31 等) は --max-minutes 絞り込みではヒットしない。
- level 充足が低いカタログが多く (85/491)、level 絞り込みの対象外が多い
  (出典に無いものを推測で補っていない)。
- nextjs_learn のタイトルは「App Router」等のコース名のみで、
  「Next.js Learn」という語自体ではヒットしない (Next.js は services に
  入っているため検索は可能)。
- cloud="その他" は28カタログ共通の値であり、ベンダー区別は cloud ではなく
  source_catalog で行う。
- CLI 実行には従来どおり `PYTHONPATH=src` が必要。
