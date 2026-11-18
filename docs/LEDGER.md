# LEDGER — クラウド学習カタログ検索エンジン

司令塔 (Muse) が管理するチェックポイント台帳。
計画: docs/PLAN.md (2026-11-18 ユーザー承認、public リポジトリ納品)

## データ分離 (public 対応, 2026-11-18)

- data/vendor/ に各社カタログ3点 (AWS 167 + Azure 550 + Google 176 = 893件) を配置済み
- 個人の学習計画386件は public に含めない。data/local/plan.json (gitignore) の
  ローカルオーバーレイとして設計し、テストは合成フィクスチャ3件で代替

## Run 1: T1 ETL + URL導線、T2 横断リンク (Devin CLI / SWE-2)

- 指示書: docs/DEVIN_RUN1_PROMPT.md
- 期待成果物: src/hands_on_search/ (ETL + link + related)、tests/ (pytest)、
  reports/devin-run1/REPORT.md (link カバレッジ実数つき)
- 合否: vendor 893件の取り込み、捏造検出テスト、Fargate 横断リンクテスト等が全通過
- 状態: 起動準備中 (台帳作成時点)

## 後続

- Run 2: T3 検索 (FTS5 trigram + 絞り込み + ゴールデンクエリ)
- Run 3: T4 推薦 + T5 CLI + README
- 納品: GitHub public リポジトリ hiyuuma/cloud-hands-on-search を司令塔が作成し
  push、Actions (T6) の通過を GitHub 側で確認してから完了報告
