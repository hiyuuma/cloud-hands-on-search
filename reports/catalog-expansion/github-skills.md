# GitHub Skills カタログ収集報告

収集日: 2026-11-18 / 収集担当: Muse (サブエージェント)
出力: `data/vendor-staging/github_skills.json` — **42件**

## 列挙方法

1. GitHub CLI (`gh api`) で skills 組織の公開リポジトリを全件列挙
   - `gh api orgs/skills` → public_repos = 53
   - `gh api "orgs/skills/repos?per_page=100"` → 53件すべて取得 (1ページで完結)
2. 公式ページ https://github.com/skills を取得し、組織の実体 (GitHub Skills 本体) と
   ピン留めコースが上記リポジトリ群と一致することを確認
3. 各コース候補のリポジトリ README を `gh api repos/skills/<repo>/readme` で取得し、
   タイトル (見出し)、所要時間 (「How long」欄)、対象者 (「Who is this for」欄) を抽出
4. 説明文はリポジトリの About (description) を使用

## 母数とカバレッジの判断根拠

skills 組織の公開リポジトリ 53件を以下の内訳で全件仕分けした (漏れなし):

| 分類 | 件数 | 内容 |
|---|---|---|
| 対話型コース (収録) | **42** | 本ファイルのレコード |
| 非推奨コース (除外) | 1 | `copilot-codespaces-vscode` — README 冒頭に Deprecation バッジがあり、後継コース `getting-started-with-github-copilot` (収録済み) への誘導が明記されているため除外 |
| 非コース (除外) | 10 | `.github` (組織プロフィール)、`exercise-template` / `exercise-creator` / `exercise-toolkit` (演習作成用基盤)、`action-update-step` / `action-check-file` / `action-text-variables` / `action-keyphrase-checker` (コース内部で使うアクション部品)、`releases` (変更履歴)、`skills-for-emu` (EMU 向けガイド文書、対話型コースではない)。いずれも各リポジトリの説明文自体が「<<Not a course>>」等と明示、または内容から明らか |

コミュニティ製の同名リポジトリは一切含めていない (所有者が skills 組織のものだけを対象とした)。

## 検証方法

- URL は全件 `https://github.com/skills/<repo>` で、組織リポジトリ一覧 API が返した
  実在 URL (html_url) そのもの。推測で組み立てた URL は無い
- 収録42件すべてについて README の API 取得が成功しており、リポジトリの実在と
  コース内容の両方を二重に確認済み
- タイトル・所要時間は README 出典、説明文はリポジトリメタデータ出典

## フィールド充足率

- url: 42/42 (必須、全件)
- duration_text: 40/42 (README に「How long」欄のあるもの。欠落は `secure-code-game` と
  `secure-repository-supply-chain` の2件)
- level: 14/42 (README の対象者欄に Beginner / Intermediate / All levels の明示があるもの
  のみ。推測での補完はしていない)

## 分類サマリ

- ドメイン: AI 17件 / CI-CD 9件 / 開発・Git 7件 / セキュリティ・IAM 5件 / その他 4件
- priority_for_user: 高 17件 / 中 15件 / 低 10件
  (高 = CI/CD・Copilot・エージェント/MCP などユーザーの日常テーマに直結、
   中 = Git 基礎・Codespaces 等、低 = 周辺・ニッチ)

## 注意事項 (統合時に要確認)

- `ai-in-actions` と `create-ai-powered-actions` は GitHub Models を題材とするが、
  GitHub Models は 2026-07-30 に提供終了済み (ユーザー側の検証済み事実)。
  公式コースとしては現存するため収録し、priority は「低」に下げて要約にも明記した
- `your-first-extension-for-github-copilot` は、題材の Copilot Extensions 自体が
  2025-11-10 に MCP への移行のため非推奨化された (README の CAUTION 出典)。
  同様に収録のうえ priority「低」とし、要約に明記した
- コースのタイトルは README 見出しを正とした。例: `change-commit-history` の
  README 見出しは "Remove commit history" (リポジトリ説明文は "changing the commit
  history" 系)。統合時にカタログ表示名と突き合わせること
