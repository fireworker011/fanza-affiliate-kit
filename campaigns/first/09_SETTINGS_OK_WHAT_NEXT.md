# Netlify設定の見方（あなたの画面の解読）

貼ってくれた内容から:

| 項目 | あなたの値 | 判定 |
|------|------------|------|
| Firewall / Published deploys | **Allow all traffic** | 正解・公開OK |
| Geographic / IP制限 | Not set | 正解 |
| WAF | Disabled | 問題なし（そのままでOK） |
| OAuth | なし | 問題なし |
| Last deploy | Netlify Drop・最近 | サイトはある |

**パスワード保護で困る状態ではない**です。  
この **Access & security** 画面はもう触らなくて大丈夫です。

「A new home for visitor access」→ **Go to visitor access** は、  
万一パスワードがONのときだけ見ればよいです。今はスキップでOK。

---

## 残っている不具合

`/css/style.css` が **404**（デザイン用ファイルがサーバーに無い）

→ 文章・リンクはあるが、見た目が素っ気ない状態。

---

## 次にクリックする場所

1. 左メニュー **Deploys**（Access & security ではない）
2. 画面の「Drag and drop your site output folder here」に  
   **ZIPを解凍した中身のフォルダ** を落とす  
   または新しい Drop: https://app.netlify.com/drop

### 推奨手順（確実）

1. エクスプローラーで開く:
   ```
   C:\Users\ys734\fanza_affiliate_kit\campaigns\first\doujin-lab-site.zip
   ```
2. ZIPを **右クリック → すべて展開**  
   展開先に次があることを確認:
   ```
   index.html
   hub.html
   review-a.html
   review-b.html
   review-c.html
   css\style.css
   ```
3. Netlify の **Deploys** で、  
   **フォルダごと**（zipそのものより中身のフォルダ）をドラッグ＆ドロップ  
4. 完了後、シークレットで:
   https://preeminent-frangipane-e8530c.netlify.app/hub.html  
5. 赤いボタン・暗い背景が出れば成功

---

## 成功後

Xプロフィールに:

```
https://preeminent-frangipane-e8530c.netlify.app/hub.html
```

文面: `03_x_posts_LIVE.md`
