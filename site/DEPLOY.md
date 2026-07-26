# ブログ代わりの静的サイト — 公開手順

フォルダ: `fanza_affiliate_kit/site/`

ローカル確認:

```powershell
cd C:\Users\ys734\fanza_affiliate_kit\site
start index.html
```

年齢確認 → トップ → 比較ハブ → 各レビュー。CTAでFANZAに着地するか確認。

---

## 公開方法（どれか1つ）

### A. Cloudflare Pages（おすすめ・無料）

1. https://pages.cloudflare.com/ でサインアップ  
2. 「Upload assets」で `site` フォルダをZIPしてアップロード  
   - または Git 連携でリポジトリを繋ぐ  
3. 公開URLが発行される  
4. そのURLを DMMアフィリエイトのサイトとして既に承認済みなら問題なし  
   - **別URLになる場合はサイト追加申請が必要**

### B. Netlify Drop

1. https://app.netlify.com/drop  
2. `site` フォルダをドラッグ＆ドロップ  
3. 発行URLを控える  

### C. GitHub Pages

1. リポジトリ作成 → `site` の中身を root または `/docs` に配置  
2. Settings → Pages で公開  
3. **アフィID入りHTMLを公開リポジトリに置くのは通常問題ない**（リンク自体が公開前提）  
   - ただしリポジトリを Private にして Pages だけ公開する運用も可  

### D. レンタルサーバー / エックスサーバー等

`site` 内ファイルを `public_html` にアップロード。

---

## 公開後すぐやること

1. スマホで年齢ゲート → ハブ → CTA を確認  
2. Xプロフィールに **ハブURL**（`hub.html` のフルURL）を設定  
3. DMM管理画面でサイトURLが公開URLと一致しているか確認（違うなら追加）  
4. 検索許可はソースで `index,follow` 済み。再デプロイ後に  
   `/robots.txt` と `/sitemap.xml` が 200 になること  


---

## 注意

- 無料ブログのアダルト禁止規約に比べ、自前静的サイトの方が自由度が高い  
- ドメインを後から付けてもOK（まずは無料URLで運用開始でよい）  
