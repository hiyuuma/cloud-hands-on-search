# Run 1 報告 — T1 (正規化ETL + URL導線) / T2 (横断リンク)

状態: 完了 (2026-11-18)

## 実装したモジュール

`src/hands_on_search/` 以下、標準ライブラリのみで実装。

| ファイル | 役割 |
|---|---|
| `normalize.py` | duration を分に変換 ("1h"→60, "1h 30m"→90, "45 minutes"→45, 空欄→None)。services を `;` `,` 分割でリスト化。タイトル正規化キー (NFKC・小文字・記号空白統一) と URL 正規化 |
| `loaders.py` | 4形式のローダ。AWS (JSON配列) / Azure (dict.items) / Google (JSON配列) / plan (オーバーレイ、ファイルが無ければスキップ)。統一スキーマへ正規化し `raw` に元レコードを保持 |
| `related.py` | T2 横断リンク。正規化タイトル一致 + direct URL 一致で異カタログ間を `related` (相互参照IDリスト) に記録。削除・マージはしない。related 先に direct URL がある場合は link を direct に格上げし `source` に引き継ぎ元カタログを記録 |
| `link_report.py` | カタログ別 direct/search/none/total の集計 (`link_report`) と Markdown 出力 (`link_report_markdown`) |
| `db.py` | SQLite データ層。`records` テーブル (T3 FTS5 の土台)、`build_db`/`load_db` で往復可能。DB ファイルは生成物で git 対象外 |
| `etl.py` | パイプライン本体 `run_etl` / `load_all`。`python3 -m hands_on_search.etl` で `build/unified.json`, `link_report.{json,md}`, `catalog.db` を生成 |

## URL 導線の振る舞い

- `link = {url, kind: direct|search|none, source}` を全レコードに付与
- direct は元データに実在する URL のみ (捏造なし。テストで機械検証)
- Azure は `url_ja` を主導線 (550/550 件 direct)
- AWS で直接 URL が無い 144 件は公式検索パターン
  `https://skillbuilder.aws/search?searchText=<quote(title)>&typeId=aws_builder_lab`
  で kind=search を生成
- Google / plan で直接 URL が無い件は確実な公式検索パターンが無いため
  kind=none (url 空) とし、link_report で可視化

## link カバレッジ実数 (vendor 893件のみ, build/ 生成物より)

| catalog | total | direct | search | none |
|---|---|---|---|---|
| aws | 167 | 23 | 144 | 0 |
| azure | 550 | 550 | 0 | 0 |
| google | 176 | 154 | 0 | 22 |

plan フィクスチャ3件込み (テスト内で計測): plan は direct 2 / none 1。
横断リンク: 2 レコードが related で結ばれ (aws Fargate ラボ ⇔ plan:HO-SAMPLE-003)、
plan 側の link が AWS の direct URL へ格上げ (source=aws) された 1 件。

## テスト結果

実行コマンド:

    .venv/bin/python -m pytest tests/ -q

結果: **16 passed** (0.24s)

内訳:
- `tests/test_etl.py` … vendor 893件 (167+550+176) 全件取り込み、plan 3件、
  ID一意、全レコードに link、direct URL が元データ URL 集合に含まれる
  (捏造検出)、AWS search パターン一致、Azure 主導線が url_ja
- `tests/test_related.py` … HO-SAMPLE-003 ⇔ AWS
  "Deploy and Scale Containerized Applications with AWS Fargate" の
  双方向 related、related の対称性、削除/マージ無し (896件維持・raw 保持)
- `tests/test_normalize.py` … duration 代表例、services 分割、タイトル正規化
- `tests/test_outputs.py` … link_report 集計整合、SQLite 往復

## 環境メモ

- pytest がシステム Python 3.12 に無かったため `.venv` (gitignore 済) を作り
  pytest のみ導入。アプリ本体の依存は標準ライブラリのみ (制約どおり)。
- `python3 -m pytest` が使えるよう `tests/conftest.py` で `src/` を
  sys.path に追加している。

## 判断した点・備考

- AWS/Google レコードには元データに ID が無いため、タイトルの安定スラッグを
  `aws:`/`google:` 接頭辞付きで採番 (ベンダータイトルは各カタログ内で一意。
  重複が将来出た場合はスラッグ衝突で検出できるよう、テストで ID 一意性を検査)。
- Azure `levels` は "intermediate;advanced" のような複数値があるため
  `level` には元の文字列を保持 (分割は T3 以降の絞り込み側で扱う想定)。
- Google の `credits` を `access` に写した (空は None)。
- AWS `plan_month` は "2027-03 データ基盤 / 分析" のように月+テーマ複合の
  値をそのまま保持 (分割はしていない)。
- 日英表記ゆれの吸収は NFKC + 小文字 + 記号正規化の範囲。意味的な同義
  (例: 「入門」vs "Getting Started") はマッチしない (既知の制限)。
- `python -m hands_on_search.etl` 実行時に runpy の RuntimeWarning が出る
  (`__init__` が etl を import するため)。動作に影響なし。
