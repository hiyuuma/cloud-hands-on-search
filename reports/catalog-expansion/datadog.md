# Datadog 学習カタログ収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/datadog.json` (**25件**)

## 使った公式ページ (列挙の母集団・裏取り)

| ページ | URL | 用途 |
|---|---|---|
| Datadog Learning Center コース一覧 | https://learn.datadoghq.com/collections | 全コースのタイトル・説明文の列挙母集団 |
| カテゴリ別コレクション | https://learn.datadoghq.com/collections/getting-started ほか (apm / logs / security / dashboards-notebooks / aws / configure-develop / opentelemetry / ux-monitoring / service-management) | カテゴリ別のタイトル・説明文の確認 |
| 各コースページ (25件) | datadog.json の各 URL | URL の実在、所要時間・レベルの確認 |
| Premium Enablement コースカタログ (PDF) | https://www.datadoghq.com/pdf/premium-enablement-course-catalog.pdf | 有料側 (講師主導) の切り分け確認 |

## 件数と充足率

- 収録件数: **25件** (すべて type=course、全件無料 — コレクションページ上で全コースに "Enroll for free" と表示される)
- duration_text 充足: 10/25件 — コースページに "X hour(s) to complete" と明記されていたもののみ原文転記
- level 充足: 9/25件 — コースページの表記 (Beginner / Intermediate) を転記
- description: 23/25件にコレクションページまたはコースページの公式説明文を設定 (2件は説明文を取得できず空欄)

優先度 (priority_for_user) の付け方: 可観測性は実務テーマのため入門・実践とも「中」。Product Analytics のみ周辺領域として「低」。

## 無料/有料の切り分け

- **無料 (収録対象)**: Datadog Learning Center (learn.datadoghq.com) のセルフペースコースは全件無料。認定試験対策のラーニングパス (Datadog Fundamentals 等) も無料で公開されている
- **有料 (収録対象外)**: 講師主導の **Premium Enablement** (datadoghq.com/technical-enablement 配下のセッション群と PDF カタログ掲載コース群。コード体系 101〜301 + ワークショップで数十セッション規模) と、認定試験そのもの (Datadog Fundamentals 等、各 100 USD の監督付き試験)。いずれも Learning Center のコースではないため収録していない

## カバレッジの限界 (正直な報告)

- Learning Center の全コース数はコレクション横断で **90件超** (コレクション間の重複を含む概数) とみられるが、本収集は **個別 URL を公式に確認できた25件のみ** を収録した。残りは URL の推測・組み立てをしない方針のため未収録 (例: Getting Started with Metrics / Understanding Service Level Objectives (SLOs) / Getting Started with Incident Management / Tagging Best Practices / Getting Started with the Datadog AWS Integration など、タイトルと説明文は公式コレクションで確認済みだが個別 URL 未確認のものが多数ある)
- コレクションページのテキスト取得では各コースへのリンク URL が露出しないため、URL は検索インデックスに載ったコースページから取得した。このため収録は検索インデックスに載っているコースに偏っている
- 廃止済みコース (Introduction to Monitoring は2023年4月廃止、Datadog 101: Developer は2025年7月廃止) は除外した
- 「Create Custom Metrics with OpenTelemetry」は旧タイトル "Create Custom Metrics with OTel" から改称されており、現在のコレクション表記を採用した

## 検証方法

1. 母集団の列挙: 公式コレクションページ群でタイトルと説明文を列挙し、全コースが無料 ("Enroll for free") であることを確認
2. URL の取得: 各コースの URL は、検索結果として返された learn.datadoghq.com 公式コースページの URL をそのまま転記 (組み立て・推測なし)
3. 実在・属性確認: 代表コースを実際に開いて内容 (Abstract / 所要時間 / レベル) を確認し、他のコースも検索インデックス上のコースページ本文 (所要時間・レベルの表記を含む) で照合した
