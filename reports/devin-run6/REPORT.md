# Run 6 報告 — link_lang (リンク先言語フラグ) の追加

状態: 完了 (2026-11-18)

前提: 既存 96 テストを壊さないこと。結果は **117 passed**
(既存 96 + 新規 21)。

## 定義

`link_lang` = 「収録されているリンク URL が指すページの言語」。
`"ja"` または `"en"`。プラットフォームに日本語版が別途存在しても、
収録リンクが英語ページなら `"en"` (リンク先の言語が定義であり、
日本語版の有無とは別)。kind=search の導線 URL も同じルールで判定。

## 判定パターン (ETL 内の決定的ルール)

`normalize.detect_link_lang(url)` に集約。実データで確認した
パターンのみ使用し、推測では埋めない:

| パターン | 該当カタログ | 件数 |
|---|---|---|
| パスセグメントが `ja` / `ja-jp` / `ja_jp` | azure (`learn.microsoft.com/ja-jp/`), anthropic (`academy.claude.com/ja/`) | 550 + 29 |
| クエリ `locale`/`hl`/`lang` の値が `ja` 始まり | google (`skills.google?locale=ja`) | 80 |
| `*.oracle.com` でパスセグメントが `japanese-` 始まり | oracle (`mylearn.oracle.com/ou/learning-path/japanese-...`) | 1 |
| 上記以外 (空 URL 含む) | 全カタログ | en |

判定は `loaders._with_link_lang` で各 `load_*` の出口に適用
(link 確定後に計算するためローダ内ではなく出口で一括付与)。

## 実測内訳 (build/unified.json 2,073件)

| catalog | ja | en |
|---|---|---|
| azure | 550 | 0 |
| anthropic | 29 | 0 |
| google | 80 | 96 |
| oracle | 1 | 88 |
| その他27カタログ + plan | 0 | 残り全部 |
| **合計** | **660** | **1,413** |

期待値 660 (azure 550 + anthropic 29 + google 80 + oracle 1) と
**完全一致**。テスト `test_link_lang_counts_fixed` で固定済み。

なおテストフィクスチャの plan 3件のうち1件は
`learn.microsoft.com/ja-jp/search` への search 導線のため、
`records` フィクスチャ (2,076件) 上の ja は 661 になる
(仕様どおり search リンクも同ルールで判定)。

## 変更内容

- `normalize.py`: `detect_link_lang(url)` 追加
- `loaders.py`: 統一スキーマに `link_lang` 追加 (`_base` 既定 "en"、
  全 `load_*` で `_with_link_lang` を適用)
- `db.py`: `records.link_lang` カラム追加 (スキーマ + `_COLUMNS`)
- `search.py`: `link_lang` フィルタ追加 (完全一致)
- `cli.py`: `search --lang ja|en` 追加、検索結果の link 行に
  `(lang: xx)` 表記、`show` に `link_lang:` 行を追加
- `web/unified-compact.json`: link_lang を含む 15キーで再生成 (2,073件)
- `README.md`: link_lang の定義と内訳を明記

## テスト

実行コマンド:

    .venv/bin/python -m pytest tests/ -q

結果: **117 passed** — 既存 96 + 新規 21 (tests/test_link_lang.py)

新規テスト内訳:
- `detect_link_lang` 単体: ja 6パターン (ja-jp / /ja/ / locale=ja /
  hl=ja / oracle japanese- / azure search URL)、en 9パターン
  (en-us / ロケールなし / 空 / None 等)
- 全件に link_lang が付くこと
- ja 件数の固定 (合計660 + カタログ別内訳)
- `search(link_lang=...)` フィルタと ja+en の全件整合
- kind=search の ja リンクが存在すること
- CLI `--lang ja`
- web/unified-compact.json に link_lang が全件付くこと・ja=660

既存テストの変更: なし (96件すべて無改変で通過)

## ETL 再生成

`PYTHONPATH=src .venv/bin/python -m hands_on_search.etl` 実行済み。
build/unified.json / link_report.{json,md} / catalog.db /
web/unified-compact.json を再生成した。

## 既知の制限

- `link_lang` は「リンク URL が明示するロケール」ベースであり、
  リンク先ページの実際の言語をクロールして検証したものではない。
  日本語ロケール表記のない日本語ページ (例: 日本語だが /ja/ を
  含まない URL) は "en" と判定される。
- oracle の `japanese-` スラグ判定は mylearn.oracle.com の
  命名規則に依存しており、将来 URL 形式が変わると検出できない
  可能性がある (件数はテストで固定しているため変化時に検知できる)。
- google の日本語版は `locale=ja` クエリで判定している。直接 URL
  (course_templates 等) はロケールを含まないため、日本語 UI で
  開ける場合でも収録リンク基準で "en" となる。
