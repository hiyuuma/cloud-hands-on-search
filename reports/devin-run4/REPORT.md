# Run 4 報告 — 新規4カタログの統合

状態: 完了 (2026-11-18)

前提: 既存 73 テストを壊さないこと。結果は **84 passed** (既存 73 + 新規 11)。
vendor 総件数は 893 → **1,582 件** (+689)。

## 統合サマリ

`data/vendor-staging/` の検証済み 4 ファイルを `data/vendor/` へ git mv し、
各カタログのローダを loaders.py に追加、etl.py の DEFAULT_PATHS / load_all
に組み込んだ。

| catalog | total | duration 充足 | level 充足 | access 内訳 | link |
|---|---|---|---|---|---|
| hashicorp | 499 | 477/499 (96%) | 0/499 | Free 499 | direct 499 |
| linux_foundation | 59 | 3/59 (5%) | 51/59 (86%) | Paid 44 / Free 9 / unknown 6 | direct 59 |
| github_skills | 42 | 40/42 (95%) | 14/42 (33%) | Free 42 | direct 42 |
| oracle | 89 | 74/89 (83%) | 9/89 (10%) | Free 89 | direct 89 |

- ID: カタログ接頭辞つき (`hashicorp:` / `linux_foundation:` /
  `github_skills:` / `oracle:`)。hashicorp は同名タイトルが製品横断・
  コレクション間で 17 組重複するため、タイトルではなく一意な URL パスから
  スラッグを取る (実データで重複 0 を確認、テストで固定)。
- cloud: 4カタログとも 3クラウド外のため PLAN の区分に従い「その他」に統一
  (元の出典情報は raw に残る)。
- level は出典の表記をそのまま保持し、空欄は推測しない (hashicorp は
  出典側が全件空欄のため level 充足 0)。
- priority / summary_ja / domain / services は staging の値をそのまま尊重
  (テストで raw との一致を検証)。

## duration 変換

`parse_duration_minutes` を拡張し、指示書の表記例 ("26h 30m" /
"1 hour, 30 minutes" / "2 hours, 15 minutes" / "45 minutes" / "15 minutes" /
"3 hours") に加え、実データに存在する以下の表記も変換できるようにした:

- `10min` / `1hr 40min` (HashiCorp)
- `less than 30 minutes` / `less than 2 hours` 等: 上限値を分で返す
- `less than one hour` / `less than an hour`: "a/an/one + 単位" の英語数詞を
  1 に変換する前処理を追加し 60 を返す
- `90–120 minutes` (レンジ表記): 後側 (上限) の値を返す
- `Duration of Exam 90 minutes` / `roughly 55 minutes`: トークン抽出で変換

**変換できなかった件数: 2 件** (いずれも linux_foundation の
`"1 day of Instructor-led class time"`)。日単位→分の換算 (1日=何時間か) は
出典に根拠がなく推測になるため、規則どおり None とした。
これとは別に duration_text 自体が空欄のもの: hashicorp 22 / LF 54 /
github_skills 2 / oracle 15 (いずれも duration_min=None、推測で埋めていない)。
上記件数は `test_new_catalog_duration_coverage` で固定した。

## billing (access) 判断の根拠

- **hashicorp (Free 499)**: developer.hashicorp.com のチュートリアルは
  公開・無料。指示書の目安どおり Free。
- **github_skills (Free 42)**: github.com/skills のインタラクティブコースは
  無料 (GitHub アカウントで実施)。指示書の目安どおり Free。
- **oracle (Free 89)**: MyLearn ラーニングパスは Oracle 公式
  "Free Training and Certifications from Oracle University"
  (reports/catalog-expansion/oracle.md に出典 URL 記録) に基づく。
  LiveLabs ワークショップも無料公開。指示書の目安どおり Free。
- **linux_foundation**: 出典の price_text から機械判定した
  (`_lf_access`)。`$0` → Free (9件)、`$<正>` → Paid (44件)、
  空欄 → unknown (6件、価格未取得のため推測しない)。価格原文は
  raw.price_text に残る。
  - 注意: access の語彙に "Paid" を新規追加した (既存は
    Subscription / Free / credits / unknown)。課金の見立て表示では
    Paid は「有料」、unknown は従来どおり「不明・要確認」として扱う。

## 導線 (link) 内訳

staging の URL は全件 kind=direct (実在確認済み)。ETL 再生成後の
link_report 実数 (vendor 1,582 件):

| catalog | total | direct | search | none |
|---|---|---|---|---|
| aws | 167 | 23 | 144 | 0 |
| azure | 550 | 550 | 0 | 0 |
| github_skills | 42 | 42 | 0 | 0 |
| google | 176 | 96 | 80 | 0 |
| hashicorp | 499 | 499 | 0 | 0 |
| linux_foundation | 59 | 59 | 0 | 0 |
| oracle | 89 | 89 | 0 | 0 |

direct 計 1,358 / search 計 224 / none 0。「direct は元データに実在する
ものだけ」の機械テスト (`test_no_fabricated_direct_urls`) の元データ集合に
新4ファイルを追加し、新カタログ由来の direct も同じ検査にかけている。

## 横断リンク (T2)

既存ルール (正規化タイトル一致 / URL 一致) を新カタログにもそのまま適用。
新規に張られた関連は 2 組のみ:

- `github_skills:introduction-to-git` ↔ `azure:learn.student-evangelism.introduction-to-git`
- `github_skills:introduction-to-github` ↔ `azure:learn.github.introduction-to-github`

両者とも双方が direct URL を持つため link の格上げは発生しなかった
(格上げ 0 件)。無理に増やしていない。

## ゴールデンクエリ実測 (build/catalog.db)

| クエリ | 条件 | 実測 |
|---|---|---|
| Terraform | HashiCorp 公式チュートリアルが上位 | 合格: top1〜3 とも hashicorp (例: "Terraform Stacks Concepts in HCP Terraform", direct=developer.hashicorp.com) |
| Kubernetes | Linux Foundation のコースがヒット | 合格: top10 内 3位に "Introduction to Kubernetes (LFS158)" (linux_foundation) |
| MCP | LiveLabs "Put AI Agents to Work with MCP" がヒット | 合格: 13件ヒット、対象レコードは 6位 ("Put AI Agents to Work with MCP and OCI Container Instances.", oracle) |

いずれも `tests/test_search.py` の新規ゴールデンテストとして機械検証。

## テスト

実行コマンド:

    .venv/bin/python -m pytest tests/ -q

結果: **84 passed** (1.4s) — Run 3 の 73 件 + 新規 11 件

新規テスト内訳:
- test_etl.py (+7): 新カタログ全件 direct、hashicorp URL パス ID の一意性、
  共通フィールドの raw 一致 (title/priority/summary_ja/services/cloud)、
  duration 代表変換、LF の price→access 判定、他3カタログ Free、
  変換不能・空欄件数の固定
- test_normalize.py (+1): Run 4 の duration 表記の単体変換
- test_search.py (+3): Terraform/Kubernetes/MCP の新ゴールデンクエリ

既存テストの更新 (件数の変更のみ、仕様の緩和なし):
- test_vendor_counts: 893 → 1,582 (4カタログ追加)
- test_no_merge_and_raw_preserved: 896 → 1,585
- _raw_url_set: 新4ファイルの url を元データ集合に追加

## ETL 再生成

`PYTHONPATH=src .venv/bin/python -m hands_on_search.etl` 実行済み。
build/unified.json (1,582 件) / link_report.{json,md} / catalog.db を更新し、
web/unified-compact.json も同じフィールド構成 (14キー) で 1,582 件に再生成
した (生成コマンドは従来どおり unified.json からの射影)。

## 既知の制限

- duration_min は「表記された所要時間」の分換算であり、"less than X" や
  "90–120 minutes" のような上限・レンジ表記は上限値を採用している
  (所要時間の下限ではない点に注意)。レンジ幅は raw.duration_text に残る。
- LF の level は "Beginner"/"Intermediate" 等の出典表記のまま
  (既存カタログ同様、大文字小文字の正規化は行っていない)。level 絞り込みは
  部分一致のため "intermediate" でもマッチする。
- LF の price_text は 2026-11-18 時点の表示価格。セールで変動し得るため
  access=Paid は「有料 (価格は原文参照)」の意味であって金額保証ではない。
- hashicorp の level は出典側が全件空欄のため、level 絞り込みでは
  ヒットしない (推測で補っていない)。
- github_skills の "AI in Actions" 等、summary_ja に「提供終了済み」と
  注記のあるレコードも収録している (元データの内容は改変しない方針)。
- cloud="その他" は4カタログ共通の値であり、OCI / HashiCorp / GitHub の
  区別は cloud ではなく source_catalog で行う。
- CLI 実行には従来どおり `PYTHONPATH=src` が必要。
