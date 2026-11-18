# Salesforce Trailhead 収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/salesforce_trailhead.json` (**22件**: trail 19件 / module 3件)

## 使った公式ページ

- Trailhead トップ/一覧: https://trailhead.salesforce.com/trails (JS描画のため一覧の機械取得は不可。本文確認用)
- 各 trail / module の公式ページ (trailhead.salesforce.com/content/learn/trails/… および /modules/…)。検索インデックスに載った公式ページの本文 (タイトル・レベル・ロール・所要時間・説明・Price: 0 USD) を出典とした
- 実在確認として Developer Beginner トレイルページを実際に開いて全文取得し、タイトル・レベル (Intermediate)・所要時間 (~14 hrs 10 mins)・価格 (0 USD) の一致を確認した

## 範囲の絞り方

- 指示どおり技術系に限定: 管理者 (Admin Beginner/Intermediate、セキュリティ、自動化)、開発者 (Developer Beginner/Intermediate、SDLC、開発基礎)、AI (Agentforce 系トレイル群、Einstein AI) を優先収録
- 営業・業務ユーザー向け汎用トレイル (Sales/Service の業務手順系、マーケティング系の大半) は対象外とした
- module は、トレイルページや検索結果でタイトル・説明が公式に確認できた3件のみ収録 (モジュール単体の網羅はしていない)

## 件数と充足率

- level 充足: 15/22件 (トレイルページに表示があるもの)
- duration_text 充足: 17/22件 (原文 "~7 hrs 20 mins" 形式で転記)
- description: 全件に公式説明文を設定
- 全件 Price: 0 USD (Trailhead は無料プラットフォームであることを各ページの Price 表記で確認)

## カバレッジの限界 (正直な報告)

- Trailhead の母数はトレイル数百件・モジュール数千件規模。本収集の22件は上限200件に対してもごく一部で、「技術系の代表的トレイル+確認できたモジュール」に限られる
- 一覧ページが JS 描画でテキスト取得できず、列挙は検索インデックスに載った公式ページ頼みになった。インデックスに載っていないトレイル/モジュールは拾えていない
- Developer Intermediate の URL は検索結果に trailmix パラメータ付きで載っていたものをそのまま使用 (同一トレイルへのリンク)。Build with Agentforce Service と Slack の2件も journey パラメータ付き URL をそのまま転記した
- 「Secure Your App」と「Secure Your Environment」は所要時間・ポイントが同一で内容も近いが、公式に別トレイルとして実在するため両方収録した

## 検証方法

1. 公式ドメイン (trailhead.salesforce.com) のページだけを対象に、検索インデックスの本文でタイトル・レベル・所要時間・説明・価格を確認
2. 代表として Developer Beginner を実際に開いて全文と突合
3. URL は検索結果に提示された完全な URL をそのまま転記し、組み立て・推測はしていない
