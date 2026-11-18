# Fortinet Training Institute 収集報告

収集日: 2026-11-18 / 担当: Muse (subagent) / 出力: `data/vendor-staging/fortinet.json` (**10件**)

## 使った公式ページ

| ページ | URL | 用途 |
|---|---|---|
| Cybersecurity Professionals 向けコース一覧 | https://www.fortinet.com/training/cybersecurity-professionals | コース体系 (Foundations / Secure Networking / SASE / Cloud Security / Security Operations 等) の確認 |
| Training Institute Library (Network Security カテゴリ等) | https://training.fortinet.com/local/library/?category=Topic%3ANetwork_Security | 現行セルフペースドコースの列挙・説明文・更新日の確認 |
| 各コースのライブラリ静的ページ (10件) | training.fortinet.com/local/staticpage/view.php?page=library_* (JSON の url 参照) | 個別 URL の実在確認 |

## 件数と内訳

- 収録件数: **10件** (全件 type = `course`、セルフペースド)
  - FortiOS Administrator (NSE 4) / SD-WAN Enterprise Administrator / Public Cloud Security Architect / FortiManager Administrator / FortiAnalyzer Administrator / FortiAnalyzer Analyst / FortiSIEM Analyst / FortiSASE Enterprise Administrator / FortiWeb Administrator / Network Security Support Engineer
- priority 内訳: 高3件 (FortiOS Administrator、SD-WAN、Public Cloud Security Architect) / 中7件
- domain: `セキュリティ・IAM` 9件 / `ネットワーク` 1件 (SD-WAN)
- level: FortiOS Administrator のみ `NSE 4` (公式コース一覧での対応付け)。他は公式ライブラリにレベル表記がないため null
- duration_text: 全件 null (ライブラリに所要時間の表記なし。講師付き版の日数はセルフペースドと異なるため転記していない)
- description: FortiOS Administrator のみ公式ライブラリの説明文を転記、他9件は取得できなかったため空

## 無料の切り分け方法

- Fortinet の公式方針として、**Training Institute Library のセルフペースドレッスンは全て無料** (公式ヘルプデスク/オーダリングガイドで確認)。有料なのはオンデマンドラボ (実機演習環境) と講師付きトレーニング、認定試験であり、本収集ではセルフペースドコースのみを対象にした
- 2026-07-15 のプログラム改編で旧体系名 (FCF/FCA 等) は NSE 1〜8 体系に置き換わっている。タイトルは現行ライブラリ表記に合わせた

## 検証方法

1. 母集団: 公式コース一覧ページと Training Institute Library のカテゴリページから現行セルフペースドコースを列挙
2. 個別 URL: ライブラリ内の旧バージョンコース表記に「Newer version available」として **公式に埋め込まれていた静的ページ URL**、または公式ページで直接確認できた URL のみを収録した (10件)。例: `library_fortios-administrator`、`library_fortisiem-analyst`、`library_public-cloud-security-architect` 等はいずれもライブラリページ本文中のリンクとして実在確認したもので、命名規則からの推測ではない
3. FortiOS Administrator の現行コース実体は FortiOS 8.0 Administrator Self-Paced (https://training.fortinet.com/course/view.php?id=92277、2026-09-18 更新) で、収録 URL の静的ページがその案内先になっている

## カバレッジの限界 (重要)

- ライブラリには無料セルフペースドコースが数十件あるが、**個別 URL が検証できた10件のみ収録**。以下は実在と無料を確認しながら URL 未検証のため未収録 (ライブブラウザでライブラリを巡回すれば回収できる見込み):
  - Foundations: Cybersecurity and Cloud Fundamentals 1.0 / Introduction to Next Generation Firewall 1.0 / **FortiGate 7.6 Operator** (説明文確認済み: FortiGate の基本操作とセキュリティ強化)
  - Secure Networking: **FortiSwitch 7.6 Administrator** (説明文確認済み: FortiLink による FortiSwitch の展開・管理、L2/L3、MCLAG)、SD-WAN 7.6 Core Administrator、FortiVoice / FortiNAC / Secure Wireless LAN / Enterprise Firewall 等
  - IAM 直結: **FortiAuthenticator 8.0 Administrator** (説明文確認済み: 安全な認証と ID 管理、証明書管理・二要素認証・LDAP/RADIUS・SAML SSO)。ユーザーの IAM テーマに最も直結するため、追加収集の最優先候補
  - その他: FortiADC 7.6 Administrator / FortiDeceptor 6.2 Administrator / FortiDLP 26 Administrator / FortiEDR 7.0 Administrator / FortiMail 7.4 Administrator / FortiMail Workspace Security 26 Administrator / FortiNDR Cloud 26.1 Analyst / FortiGate 7.4 Chassis Administrator / OT Security 7.6 Architect 等
- コースのバージョンアップが頻繁で、旧バージョンは「OLDER VERSION」として残る。収録は現行版への案内ページに統一した

## 追補 (2026-11-18、ブラウザ追加収集)
未収録だった3件 (FortiAuthenticator 8.0 Administrator / FortiSwitch 7.6 Administrator / FortiGate 7.6 Operator) の詳細ページを実ブラウザで確認し fortinet.json に追加 (計13件)。所要時間は各ページの Course Duration 原文 (18h / 18h / 8h、Authenticator は講義12h+ラボ6h)。レベル表示は同サイトにないため空欄。分類は司令塔 (Muse) が付与。
