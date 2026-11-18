# cloud-hands-on-search

3クラウド (AWS / Azure / Google) の学習カタログを統合し、日本語で検索・推薦でき、
見つけたらその場で始められる URL 導線が必ず付く検索エンジン。

開発中です。計画と進捗は docs/PLAN.md と docs/LEDGER.md を参照してください。

## データについて

- data/vendor/ の各社カタログは、公式カタログ (AWS Skill Builder / Microsoft Learn /
  Google Skills) の公開情報をもとに作成したメタデータです
- 個人の学習計画はこのリポジトリに含みません。手元の計画ファイルは
  data/local/plan.json に置くとローカルオーバーレイとして取り込まれます
  (data/local/ は .gitignore 対象です)

## URL導線について

全レコードに link が付きます。kind=direct はラボへの直行URL (元データに実在する
もののみ)、kind=search は公式検索への導線です。直接URLを推測で作ることはしません。
