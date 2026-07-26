# FANZA アフィリエイト スターターキット

ゼロから FANZA（DMMアフィリエイト）で稼ぐ導線を組むための **初心者向け一式** です。  
市場リサーチ → 環境構築 → 登録・リンク取得 → 稼ぎやすい構造 → 文章/動画でクリックさせる方法まで、順番に進められます。

## 使い方（最短）

### すでに登録・承認済みで商品リンクがある場合（最優先）

1. **完成サイトを開く:** [`site/index.html`](site/index.html)  
2. **公開する:** [`site/DEPLOY.md`](site/DEPLOY.md)  
3. **X投稿:** [`campaigns/first/03_x_posts.md`](campaigns/first/03_x_posts.md)  
4. 進捗: [`campaigns/first/00_PROGRESS.md`](campaigns/first/00_PROGRESS.md)  
5. レビュー差別化: [`docs/06_grok_review_method.md`](docs/06_grok_review_method.md)  

初回キャンペーンは **FANZA同人3作品**（水渡さん / 姉弟長尺 / ギャル化）で構築済み。

**公開URL:** https://preeminent-frangipane-e8530c.netlify.app/  
**ハブ（X用）:** https://preeminent-frangipane-e8530c.netlify.app/hub.html  
**公開後チェック:** [`campaigns/first/06_LIVE_URL.md`](campaigns/first/06_LIVE_URL.md)  
**クリック0の原因と改善:** [`campaigns/first/11_ZERO_CLICK_DIAGNOSIS.md`](campaigns/first/11_ZERO_CLICK_DIAGNOSIS.md)  
**note成長（連載）:** [`campaigns/first/12_NOTE_GROWTH_PACK.md`](campaigns/first/12_NOTE_GROWTH_PACK.md)  
**再デプロイ手順:** [`campaigns/first/13_DEPLOY_AND_SELFTEST.md`](campaigns/first/13_DEPLOY_AND_SELFTEST.md)  
**note日次自動化:** [`automation/README.md`](automation/README.md) — `python automation\run_daily.py`  
**PCオフでも毎日生成:** [`automation/CLOUD_DAILY.md`](automation/CLOUD_DAILY.md)（GitHub Actions）
**Xを使わない集客:** [`campaigns/first/10_NO_X_TRAFFIC.md`](campaigns/first/10_NO_X_TRAFFIC.md)

### ゼロから読む場合

1. このフォルダを開く
2. [`docs/01_runbook.md`](docs/01_runbook.md) を **STEP 0 から順に** 実行する
3. 各 STEP の **Done when** を満たしたら次へ
4. 迷ったらチェックリストで状態確認:
   - [`checklists/first_campaign.md`](checklists/first_campaign.md)
   - [`checklists/compliance.md`](checklists/compliance.md)

## キット構成

| ID | ファイル | 内容 |
|----|----------|------|
| runbook | `docs/01_runbook.md` | ゼロからの手順書（Done when 付き） |
| market_research_funnel | `docs/02_market_research_funnel.md` | ニッチ選定・需要調査・稼ぎ直結マップ |
| environment_links | `docs/03_environment_and_links.md` | アカウント・媒体・リンク作成 |
| article_template | `templates/fanza_article_template.md` | FANZA 記事テンプレ（CTA 3箇所） |
| text_click_method | `docs/04_text_click_methods.md` | 文章でリンクを踏ませる方法 |
| video_click_method | `docs/05_video_sns_click_methods.md` | 動画・SNS で踏ませる方法 |
| compliance | `checklists/compliance.md` | 年齢・規約・画像ルール |
| first_campaign | `checklists/first_campaign.md` | 初回キャンペーン総チェック |

補助テンプレ:

- `templates/fanza_ranking_template.md` … ランキング/比較記事
- `templates/fanza_beginner_guide_template.md` … 初心者ガイド（新規登録狙い）
- `templates/x_post_templates.md` … X 投稿文例

## キット健全性チェック

```powershell
cd C:\Users\ys734\fanza_affiliate_kit
python scripts\check_kit.py
python scripts\verify_plan.py
python scripts\test_check_kit.py
python scripts\test_verify_plan.py
```

- `check_kit.py` … 必須セクションの有無（exit `0` = PASS）
- `verify_plan.py` … プランの Verification 全体（ランブック順・CTA・公式URL含む）
- テストは本番チェッカーを直接駆動（再実装なし）

## 公式参照（登録・リンク・報酬）

- 公式トップ: https://affiliate.dmm.com/
- はじめてガイド: https://affiliate.dmm.com/guide/diagram
- 広告作成の基本: https://affiliate.dmm.com/guide/diagram/ad
- ツールバー: https://affiliate.dmm.com/guide/diagram/toolbar
- 報酬料率: https://affiliate.dmm.com/fee/rate/
- ヘルプ（アフィリエイト）: https://support.dmm.com/affiliate

> **地域ブロック注意**: 一部環境では `affiliate.dmm.com` が「この地域から利用できません」と表示されることがあります。日本国内の通常ブラウザ/VPNなし回線でアクセスしてください。

## スコープ外（このキットがやらないこと）

- あなたの代わりの DMM 本登録・審査通過・入金
- 本番 WordPress のホスティング契約・ドメイン購入
- 成人向け画像・動画素材の配布
- 収入保証・検索順位保証
- FANZA/DMM への ToS 違反スクレイピング

## 推奨ワークフロー（1〜2週間イメージ）

```
Day 1-2  市場リサーチ + ニッチ決定 + 媒体用意
Day 3    DMM会員 + アフィリエイト申請（記事2本以上用意してから）
Day 4    審査待ちの間にテンプレ記事を下書き
Day 5    リンク取得 → 記事に CTA 設置 → 公開
Day 6-14 X/検索で入口を回し、クリックと成約を見て改善
```

詳細は必ず `docs/01_runbook.md` を正とします。
