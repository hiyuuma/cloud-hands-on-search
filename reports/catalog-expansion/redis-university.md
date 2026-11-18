# Redis University 収集レポート（第2波）

- 収集日: 2026-11-18
- 出力: `data/vendor-staging/redis_university.json`
- 総件数: **4件**（すべて Learning Path、全件無料）

## 使った公式ページ

- 公式紹介ページ: https://redis.io/tutorials/university/ （現行ラインナップ4件の掲載と各パスへのリンクの出典）
- プラットフォーム: https://university.redis.io/ （2024-09-18 にリニューアルされた現行基盤）

## 検証方法

1. redis.io 公式の University 紹介ページに掲載された4つのラーニングパスについて、同ページのアウトリンクから university.redis.io 上の実URLをそのまま記録した（URLの推測・組み立てなし）。
2. 各パスはクイズ80%以上で修了証が発行される無料コースであることを公式ページで確認。
3. duration_text と level は公式ページに掲載がないため全件空欄。

## 収録内容

- Get Started with Redis（旧 RU101 の後継にあたる入門パス）
- Get Started with Redis Cloud
- Get Started with Redis Software
- Operate Redis Cloud

## カバレッジの限界

- **現行ラインナップは4件のみ**。旧 Redis University の RU101、Redis Security (RU330)、Running Redis at Scale、Redis Developer Certification 等は廃止済み（認定は2024年6月に deprecated）のため収録していない。
- Redis 公式ブログ（2026年1月）や第三者レビューには "Develop with Redis" パスや検索/AI 系パスの言及があるが、公式ページのテキスト取得では直接URLを検証できなかったため、捏造回避のルールに従い未収録とした。プラットフォーム側はログイン必須でコースページがリダイレクトされるため、ブラウザでの追加確認が可能な環境なら回収できる可能性がある。
- リニューアル直後でコース数が少なく、今後拡充される見込み。定期的な再確認が望ましいソース。
