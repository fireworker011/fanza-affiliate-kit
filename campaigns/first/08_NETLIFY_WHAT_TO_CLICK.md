# そのURLの画面で何をするか

あなたが開いているページ:

```
https://app.netlify.com/projects/preeminent-frangipane-e8530c/configuration/access
```

これは **Visitor access（訪問者の入場制限）** の設定画面です。  
サイトの文章やデザインを直す画面では **ありません**。

---

## 結論（先に）

| やりたいこと | このAccess画面でやる？ |
|--------------|------------------------|
| パスワード解除 | はい（保護がONのときだけ） |
| デザイン直す（CSS） | **いいえ → Deploysへ** |
| XにURL貼る | **いいえ → ブラウザでサイト確認後Xへ** |

いまサイト本体は外部から読める状態です。  
足りないのは主に **CSSの再アップロード** です。

---

## A. Access画面にいるとき（パスワード）

画面の中を見て、次のどれか。

### パターン1: 「None」「No protection」「Not protected」「—」など

→ **何もしなくてOK。**  
→ 下の **B. Deploys** に進む。

### パターン2: 「Basic password」「Team login」と書いてある

1. **Configure Password Protection**（または Configure / Edit）をクリック  
2. 保護をやめる選択肢があればそれを選ぶ  
   - None / Remove protection / 無効 など  
3. **Save**

### パターン3: 設定がグレーで触れない（Freeプランでロック）

→ この画面では外せないことがある。  
→ **サイトを削除せず、新規Dropで別URLを作る**（下の C）。

パスワードを「思い出す」「入力する」必要は **基本的にない**。  
やるのは「保護をオフ」か「保護なしで出し直す」だけ。

---

## B. デザイン修正（いま本当に必要な作業）

1. 同じサイトの画面で、左メニューまたは上の  
   **Deploys** をクリック  
   （Access / configuration から出る）

2. ブラウザで別タブを開く:  
   https://app.netlify.com/drop

3. エクスプローラーでこのZIPをドラッグ:  
   ```
   C:\Users\ys734\fanza_affiliate_kit\campaigns\first\doujin-lab-site.zip
   ```
   ※中に `css/style.css` が入っている版

4. **同じサイトに上書きしたい場合**  
   - サイトの Deploys ページに「drag and drop your site output folder here」があれば、  
     ZIPを**解凍したフォルダ**、またはZIPをそこに落とす  
   - Dropで **新しいURL** ができた場合は、その新URLを使う

5. 1分待ってからシークレットで開く:  
   https://preeminent-frangipane-e8530c.netlify.app/hub.html  
   → 色付きのボタン・暗い背景ならCSS成功

---

## C. Accessがロックされて困ったとき

1. https://app.netlify.com/drop  
2. `doujin-lab-site.zip` をドロップ（パスワード設定はしない）  
3. 出た **新しいURL** をチャットに貼る  
4. 古いサイトは後で削除してよい

---

## D. 成功したらやること

1. ハブが普通に見える  
2. Xプロフィールに:

```
https://preeminent-frangipane-e8530c.netlify.app/hub.html
```

文面: `03_x_posts_LIVE.md`

---

## 画面の言葉が英語のとき対応表

| 英語 | 意味 |
|------|------|
| Project configuration | プロジェクト設定 |
| Access & security | アクセスとセキュリティ |
| Visitor access | 訪問者アクセス |
| Password Protection | パスワード保護 |
| Configure | 設定を変更 |
| Deploys | 公開履歴・再アップロード |
| None / No protection | 保護なし（これが正解） |
