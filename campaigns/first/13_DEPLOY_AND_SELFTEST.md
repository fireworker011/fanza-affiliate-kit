# 再デプロイ & 自己クリック試験（ログイン必須・最短）

改善版ソースはローカルに準備済み。  
**Netlifyに上げないと公開URLには反映されない。**

## 1. 再デプロイ

フォルダ:

```
C:\Users\ys734\fanza_affiliate_kit\campaigns\first\deploy_folder
```

含むもの:
- 全HTML（noindexなし / sticky CTA / 年齢ゲート）
- css/style.css
- js/age-gate.js
- robots.txt
- sitemap.xml

手順:
1. https://app.netlify.com/projects/preeminent-frangipane-e8530c/deploys  
2. `deploy_folder` をドラッグ＆ドロップ  
3. 完了後ハードリロード

## 2. 公開確認URL

| 確認 | URL |
|------|-----|
| 年齢ゲート強制 | https://preeminent-frangipane-e8530c.netlify.app/hub.html?age=reset |
| robots | https://preeminent-frangipane-e8530c.netlify.app/robots.txt |
| sitemap | https://preeminent-frangipane-e8530c.netlify.app/sitemap.xml |
| sticky CTA | ハブ下部に固定ボタン |

## 3. 自己クリック試験

1. シークレットでハブを開く  
2. 「公式で詳細を見る」を1回押す  
3. FANZA商品に着地すること  
4. 翌日DMMアフィリエイトレポートにクリックが出るか見る  

出ない場合: サイト未承認URL・リンク破損・レポート遅延を疑う。

## 4. note

`12_NOTE_GROWTH_PACK.md` の連載①から順に公開。
