# 初回キャンペーン計画（確定版）

## 状態

| 項目 | 内容 |
|------|------|
| DMMアフィリエイト | 登録・**サイト承認済み** |
| af_id | fireworker-003 |
| ブログ | 未所持 → **静的サイト `site/` を用意済み** |
| ニッチ | FANZA同人 · 欲求タイプ別3択（Grok式） |
| レビュー差別化 | 5レイヤー法（`docs/06_grok_review_method.md`） |

---

## 商品（ユーザー提供リンク）

| 枠 | 作品 | 品番 | サークル | 主ラベル | アフィリンク |
|----|------|------|----------|----------|--------------|
| **入口推し** | エロ小説みたいな青春Hを陽キャ彼女の水渡さんと | d_490055 | カームホワイト | SWEET | 下記 LINK_A |
| 長尺 | 姉弟でシたらいけません | d_738506 | 柵野14 | TABOO+VOLUME | LINK_B |
| ギャップ | ボーイッシュ幼馴染がギャル化してから勃起が止まらない！ | d_692288 | なのかえいち | GAP | LINK_C |

### LINK_A (d_490055)

```
https://al.fanza.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fdc%2Fdoujin%2F-%2Fdetail%2F%3D%2Fcid%3Dd_490055%2F&af_id=fireworker-003&ch=search_link&ch_id=link
```

### LINK_B (d_738506)

```
https://al.fanza.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fdc%2Fdoujin%2F-%2Fdetail%2F%3D%2Fcid%3Dd_738506%2F&af_id=fireworker-003&ch=search_link&ch_id=link
```

### LINK_C (d_692288)

```
https://al.fanza.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fdc%2Fdoujin%2F-%2Fdetail%2F%3D%2Fcid%3Dd_692288%2F&af_id=fireworker-003&ch=search_link&ch_id=link
```

---

## サイト構成（実装済み）

```
site/index.html      トップ + 年齢ゲート
site/hub.html        比較ハブ + 30秒診断 + CTA×3系統
site/review-a.html   水渡さん
site/review-b.html   姉弟長尺
site/review-c.html   ギャル化
site/css/style.css
site/DEPLOY.md       公開手順
```

公開後URL（確定）:

```
トップ: https://preeminent-frangipane-e8530c.netlify.app/
ハブ:   https://preeminent-frangipane-e8530c.netlify.app/hub.html
```

※2026-07-20 時点で Netlify パスワード保護がONの場合あり。OFF必須。

---

## 導線

```
X投稿 → プロフィールの hub.html
  → 診断 or 比較表
  → 各レビュー
  → al.fanza.co.jp アフィリンク → FANZA商品
```
