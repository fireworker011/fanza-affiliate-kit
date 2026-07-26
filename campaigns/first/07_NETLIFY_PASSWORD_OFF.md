# Netlify パスワードが分からないとき

**パスワードを思い出す必要はありません。**  
やることは「保護を切る」か「保護なしで出し直す」だけです。

アフィ用サイトは **パスワードなし（誰でも閲覧可）** が正解です。

---

## 方法1: 管理画面で保護をOFF（おすすめ）

1. ブラウザでログイン  
   https://app.netlify.com/

2. サイト一覧から  
   `preeminent-frangipane-e8530c`  
   （または自分のサイト名）をクリック

3. 上メニューまたは左の  
   **Project configuration**（プロジェクト設定）

4. **Access & security**（アクセスとセキュリティ）

5. **Visitor access** の中の  
   **Password Protection**

6. **Configure Password Protection**（設定を変更）

7. 次のどちらか:
   - **None / No protection / 保護なし** があればそれを選ぶ  
   - または **Customize** して保護を無効にする  
   - 「Basic password」や「Team login」が入っているなら **外す / 削除 / None**

8. **Save** で保存

9. シークレットウィンドウ（Ctrl+Shift+N）で確認  
   https://preeminent-frangipane-e8530c.netlify.app/hub.html  

   → パスワード画面が出ず、年齢確認が出れば成功

### 設定URLの目安（ログイン後）

サイトを開いたあと、アドレスがだいたい次の形になります:

```
https://app.netlify.com/projects/preeminent-frangipane-e8530c/configuration/access
```

`projects` のあとの名前は自分のサイト名に読み替え。

### チーム全体のデフォルトがかかっている場合

1. 左上のチーム名 → **Team settings**  
2. **Access & security** → **Visitor access**  
3. **Default Password Protection** を確認  
4. 全サイト保護になっているなら、Owner 権限で **None / 無効** にする  
   またはサイト側で **Customize this site's protection settings** → 保護なし

※ Free 以外のプランやチーム設定で「デフォルト保護」がONのことがあります。

---

## 方法2: パスワードを「見ない・使わない」で出し直す

保護の場所が分からないときは、**新しいサイトとして再アップロード**が早いです。

1. https://app.netlify.com/drop を開く  
2. このZIPをドラッグ  
   ```
   C:\Users\ys734\fanza_affiliate_kit\campaigns\first\doujin-lab-site.zip
   ```
3. **途中で Password / Protect を聞かれたら何も設定しない・スキップ**  
4. 新しいURLが発行される  
5. 古いサイトは後で削除してOK  

新しいURLができたら、そのURLをチャットに貼ってください。X文面を差し替えます。

---

## 方法3: 画面に出ているパスワード入力は無視

サイト本体の「Please enter your password」は  
**Netlifyが付けた門番**です。

- サイトの中に書いたパスワードではない  
- キット側（HTML）にもパスワードは入っていない  
- **分からなくて正常**（自分が設定した記憶がなくても、Drop時やチーム設定で付くことがある）

---

## うまくいかないときチェック

| 症状 | やること |
|------|----------|
| 設定メニューが英語 | 上記の英語メニュー名で探す |
| Password Protection が見えない | Team settings の Default を見る |
| 権限がない | サイトを作ったGoogle/GitHubアカウントでログインし直す |
| まだ401 | 別ブラウザのシークレットで再確認（キャッシュ） |
| どうしても無理 | 方法2で新規Drop |

---

## 成功の定義

シークレットウィンドウで次が **パスワードなし** で開く:

https://preeminent-frangipane-e8530c.netlify.app/hub.html

そのあと `03_x_posts_LIVE.md` の文面でXを更新すれば運用開始です。
