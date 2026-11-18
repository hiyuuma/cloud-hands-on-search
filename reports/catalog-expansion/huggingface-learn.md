# Hugging Face Learn カタログ収集報告

収集日: 2026-11-18 / 収集担当: Muse (サブエージェント)
出力: `data/vendor-staging/huggingface_learn.json` — **12件**

## 使った公式ページ

- ハブ: https://huggingface.co/learn (JS 描画のためテキスト取得では一覧を読めず、各コースページを個別に取得して実在確認した)
- 各コースの導入ページ (全件取得してタイトル・内容・無料表記を確認):
  - LLM Course — https://huggingface.co/learn/nlp-course
  - AI Agents Course — https://huggingface.co/learn/agents-course
  - Model Context Protocol (MCP) Course — https://huggingface.co/learn/mcp-course
  - Context Course — https://huggingface.co/learn/context-course
  - a smol course — https://huggingface.co/learn/smol-course
  - Deep Reinforcement Learning Course — https://huggingface.co/learn/deep-rl-course
  - Community Computer Vision Course — https://huggingface.co/learn/computer-vision-course
  - Audio Course — https://huggingface.co/learn/audio-course
  - Diffusion Models Course — https://huggingface.co/learn/diffusion-course
  - Robotics Course — https://huggingface.co/learn/robotics-course
  - Machine Learning for Games Course — https://huggingface.co/learn/ml-games-course
  - Machine Learning for 3D Course — https://huggingface.co/learn/ml-for-3d-course

## 件数と内訳

- 収録: **12件** (全件 type=course、全件無料)
- priority_for_user: 高 3件 (Agents / MCP / Context) / 中 2件 (LLM / smol) / 低 7件
- level 充足: 3/12件 — "from beginner to expert" と明記された Agents / smol / Deep RL のみ転記。他は公式ページにレベル表記がなく null
- duration_text 充足: 8/12件 — 各コースの推奨ペース表記 (例: "approximately 3-4 hours of work per week") を原文転記。CV / Audio / ML Games / ML 3D は所要時間表記なし

## 検証方法

- 候補パスのうち `ml-3d-course` は 404 だったため、検索で公式ユニットページの実在 URL (`ml-for-3d-course`) を特定してからコーストップを開き、タイトル一致を確認した。推測で組み立てた URL は収録していない
- 無料であることは各コースページの表記で確認 (例: LLM Course "It's completely free and without ads"、Agents / MCP / smol は認定プロセスまで "completely free"、Audio は "100% free, public and open-source")。HF Learn は有料コース自体が存在しない
- 説明文は各コース導入ページの冒頭説明を出典として要約転記した

## カバレッジの限界

- ハブページが JS 描画でテキスト取得できなかったため、母数の確定は「各コースページの相互参照 (前提コースとしての言及) + ハブ掲載コースを扱う複数資料との突合」で行った。現在のハブ掲載は上記12コースで一致する
- ハブに併載される **Open-Source AI Cookbook** はノートブック集であり、コース単位の構成ではないため対象外とした
- チャプター/ユニット単位では収録していない (コース単位のみ、指示どおり)
- Deep RL Course は公式ページに low-maintenance 化の告知あり (Unit 7 とリーダーボードは機能停止)。ML for Games Course も新規ユニット追加なし・認定なしと公式に明記されている。いずれも教材自体は現行公開中のため収録した
