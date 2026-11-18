# PLAN — クラウド学習カタログ検索エンジン (cloud-hands-on-search)

状態: 2026-11-18 ユーザー承認済み（public リポジトリで発注）。
司令塔: Muse / 主実装: Devin CLI (SWE-2, ローカル実行, 無料枠は 2026-11-30 まで)

## 目的

3クラウドの学習カタログを統合し、日本語で検索・推薦でき、見つけたらその場で
始められる導線 (URL) が必ず付く検索エンジンを作る。同伴型ハンズオンの
「次にやる1本」を、所要時間と課金の見立て付きで即選べるようにする。

## 入力データ (実測値, 2026-11-18 司令塔が照合)

public リポジトリに同梱する各社カタログ (data/vendor/):

| カタログ | ファイル | 件数 | 直接URL | 備考 |
|---|---|---|---|---|
| AWS Builder Labs | aws_builder_labs.json (配列) | 167 | 23件 (13%) | 所要時間は124件分 |
| Microsoft Learn (Azure) | azure_learn.json (dict, items キー) | 550 | 550件 (100%), url_ja も全件 | Applied Skills 37件含む。評価系は duration 空欄 |
| Google Skills | google_skills.json (配列) | 176 | 154件 (87%) | 無い22件は profile 経由 |

個人の学習計画カタログ (386件) は個人の優先度・進捗・計画月を含むため
public リポジトリには含めない。代わりにローカルオーバーレイとして設計する:
- 利用者が data/local/plan.json (gitignore 対象) に置けば取り込む
- テストは tests/fixtures/plan_sample.json (合成フィクスチャ3件) で行う
- ローカルでは計画386件を取り込むと合計 1,279件になる

## 統一スキーマ (1レコード)

- id: ソース横断で一意 (例: aws:..., azure:..., google:..., plan:...)
- source_catalog: aws | azure | google | plan
- title / title_ja (あれば) / summary_ja
- cloud: AWS | Azure | GCP | その他 (元の値を raw に保持)
- services: 文字列の配列に正規化
- domain / level
- duration_min: 分に正規化。不明は null (推測で埋めない)
- access: Subscription / Free / credits 等、元の表記を保持
- priority: 高/中/低 (無いカタログは null)
- plan_month / plan_theme (あれば)
- link: {url, kind, source} — 下記 URL 導線仕様
- raw: 元レコード全体

## URL導線仕様 (必須要件, ユーザー指示 2026-11-18)

- 検索・推薦の全出力に必ず link を付ける。Markdown 書き出しではタイトルをリンクにする
- kind は direct (ラボ本人への直行URL) と search (公式検索への導線) を厳密に区別する
- 直接URLを捏造しない。direct は元データに実在する URL のみ
- Azure は url_ja を主導線にする
- AWS の直接URLが無い144件は、元カタログの出典記録で実在を確認済みの公式検索
  パターン https://skillbuilder.aws/search?searchText=<タイトル>&typeId=aws_builder_lab
  で search 導線を生成する
- 横断リンク (T2) で他カタログの direct URL を引き継げる場合は direct に格上げし、
  出典 (source) に引き継ぎ元を記録する
- ビルド時にカタログ別の direct/search 件数レポートを出す (link_report)

## チケット

- T1 正規化ETL + URL導線: 4形式→統一スキーマ。合否 = vendor 893件が1件も落ちず
  取り込める、plan フィクスチャ3件が取り込める、全レコードに link がある、
  direct URL が元データと一致する (捏造検出テスト)
- T2 重複・横断リンク: タイトル正規化 (日英・記号ゆれ・大小) と URL 一致で突合。
  削除せず link/related に記録するだけ。合成フィクスチャの Fargate 例
  (plan HO-SAMPLE-003) が AWS カタログの同名ラボとリンクされることをテストする
- T3 検索: SQLite FTS5 (trigram) で日本語部分一致。絞り込み = cloud / domain /
  service / level / duration 上限 / access / priority / plan_month。
  合否 = ゴールデンクエリ (Fargate, MCP, PostgreSQL, Kubernetes 等) で
  期待レコードが上位に入る
- T4 推薦: 空き時間・月のテーマ (11月=コンテナ, 12月=ネットワーク/IAM)・
  関心キーワードを入力し、同伴型フォーマット「今日の流れと所要時間・課金の
  見立て」付きで候補を返す。スコアリングは決定論的でテスト可能に
- T5 CLI: search / recommend / show / stats / link-report コマンドと
  セッション計画の Markdown 書き出し、README
- T6 GitHub: Actions で pytest + ゴールデンクエリ + link レポートを push 時に
  自動検証。最終納品は public リポジトリ hiyuuma/cloud-hands-on-search
  (作成と push は司令塔が行い、GitHub 側で検証してから完了報告する)
- T7 Muse スペース版 UI (2026-11-18 ユーザー追加指示):
  GitHub 版 (CLI) とは別に、Muse のスペースでも使えるようにする。
  - 形式: 統一データ (unified) を同梱した静的スペース。検索・絞り込み・推薦は
    ブラウザ内 (クライアントサイド) で完結させ、サーバーや外部送信は持たない
  - 機能: キーワード検索 (日本語部分一致)、絞り込み (cloud / domain / 所要時間 /
    access / priority / plan_month)、空き時間とテーマからの推薦表示、
    全件タイトルに URL 導線 (direct / search の種別バッジつき)
  - 推薦スコアリングは T4 と同じ決定論的ルールを JS に移植し、CLI 版と
    結果が大きく食い違わないことを確認する
  - スペースは既定で非公開 (Muse 内のみ)。公開リンク化はユーザーの別途承認後
  - 着手は T1 の統一データが検収できてから。見た目の質も完成条件に含める

## 技術方針

- Python 3.12 標準ライブラリ中心 (SQLite FTS5)。外部依存は pytest のみ可
- DB ファイルは生成物として git に含めない。再生成コマンドを用意する
- テストは pytest。すべての合否条件はテストで機械検証できる形にする
