# MongoDB University 収集レポート（第2波）

- 収集日: 2026-11-18
- 出力: `data/vendor-staging/mongodb_university.json`
- 総件数: **21件**（すべて Learning Path、全件無料・セルフペース）

## 使った公式ページ

- カタログ: https://learn.mongodb.com/catalog （Thought Industries 基盤。学習パス一覧・所要時間・説明文の出典）
- 各ラーニングパスの個別ページ（21件すべてを実際に開いてタイトルとURLを照合）

## 検証方法

1. 公式カタログページの取得結果に含まれるアウトリンク（View Details）を1件ずつ辿り、遷移先ページのURLとタイトルを記録した。URLの推測・組み立ては一切していない。
2. 実際に、素朴なスラッグ推測では当たらないケースが複数あった（例: MongoDB Atlas Administrator Path の実URLは `.../mongodb-atlas-admin-certification-learning-path`、MongoDB C# Developer Path は `.../using-mongodb-with-c-sharp`）。実地確認が必須だった証左。
3. duration_text はカタログ表示の原文（例: "20 Hours"、"4.25 Hours"）をそのまま記録。description は各パスページ冒頭の公式説明文からの抜粋。
4. level は公式ページに明示がないため全件空欄。

## 収録内容

- 開発者パス5件（Python / Node.js / Java / C# / PHP、各20時間、Associate Developer認定対応）
- 言語別入門パス5件（Using MongoDB with Python / Node.js / Java / C# / PHP、3〜4時間）
- 管理・運用系3件（Atlas Administrator 13h、Database Admin (Self-Managed) 13h、Atlas Essentials 12.5h）
- データモデリング2件（Data Modeling Path 8h、Data Modeling Skills for Developers 4.25h）
- 検索系2件（MongoDB Search 7.75h、MongoDB Vector Search 6h）
- GenAI系3件（Building GenAI Apps 7.5h、Deploying and Evaluating GenAI Apps 2h、MongoDB GenAI Developer 2h）
- MongoDB for SQL Professionals 8h

## カバレッジの限界

- **スコープ**: 指示どおりコース/パス単位に限定。カタログにはこの他に Skill（短編バッジ、例: "9.0 Overview" 45分、"Governance for AI Agents" 等）、Unit、Video、Article が多数あるが、パス構成要素または細粒度コンテンツのため収録していない。Skill は独立受講可能なものもあり、将来の追加収集候補。
- **除外したもの**: "Onboarding with Customer Success"（顧客ごとにキュレーションされるパスで一般向けコースではないため）、Instructor Led の Event 群（OA640、DEV500 等。有料クラスルーム形式のため無料セルフペースの対象外）。
- カタログは新着順表示で取得範囲が先頭ページ相当だったが、Learning Path のアウトリンクは21件すべて（上記の除外1件を除く全パス）を辿り切った。パス以外の種別については網羅性を確認していない。
