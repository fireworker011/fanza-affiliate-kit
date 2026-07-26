# 次の15分でやること（公開まで）

サイト本体・アフィリンク・レビューは **もう完成** しています。  
残るのは「ネットに置く → XにURLを書く」だけです。

---

## 手順A（いちばん簡単）Netlify Drop

1. ZIPを開くエクスプローラでここを表示:
   ```
   C:\Users\ys734\fanza_affiliate_kit\campaigns\first\doujin-lab-site.zip
   ```
2. ブラウザで開く: https://app.netlify.com/drop  
3. ZIPをドラッグ＆ドロップ（アカウント作成を求められたら無料でOK）  
4. 発行されたURLをコピー（例: `https://xxxx.netlify.app`）  
5. そのURLのあとに `/hub.html` を付けたものが比較ハブ  
   - 例: `https://xxxx.netlify.app/hub.html`

---

## 手順B Cloudflare Pages

1. https://pages.cloudflare.com/  
2. Upload assets → `doujin-lab-site.zip` をアップロード  
3. 発行URL + `/hub.html` がハブ

---

## 公開URLが取れたら（コピペ用）

下の `YOUR_BASE` を差し替え:

```
トップ: https://YOUR_BASE/
ハブ:   https://YOUR_BASE/hub.html
```

### Xプロフィール

```
FANZA同人の買い分け（あまあま/ギャップ/長尺）
Grok式で「誰向けか」だけ先に書く
▼比較
https://YOUR_BASE/hub.html
```

### 固定ポスト

```
【固定】同人をランキングだけで選ぶと事故る
30秒診断つき比較
https://YOUR_BASE/hub.html
※アフィリエイトを含みます
```

### 投稿1本目

```
同人、失敗しがちなのって
「人気＝自分向き」だと思い込むこと。

欲求の型で3作品に振り分けた
https://YOUR_BASE/hub.html
```

---

## DMM側

- 公開URLが **申請済みサイトURLと違う** 場合 → アフィリエイト管理画面でサイト追加  
- 同じドメイン/許可された媒体ならそのままでOKなこともある（表示を確認）

---

## ローカル再確認（公開前）

```powershell
cd C:\Users\ys734\fanza_affiliate_kit\site
python serve_local.py
```

ブラウザが開き、http://127.0.0.1:8765/index.html で年齢ゲートから試せます。

---

## こちらに戻すとき

公開URL（例: `https://something.netlify.app`）を1行貼ってください。  
→ `noindex` 解除版の用意、X文面の確定、進捗チェックをこちらで仕上げます。
