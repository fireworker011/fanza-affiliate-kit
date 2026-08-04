# 投稿チェックリスト（2026-08-04）

## 1. 本文
- [ ] `article.md` を note 新規投稿に貼る
- [ ] タイトル: ギャップものが刺さる人の条件

## 2. 画像
- [ ] `images/01_prompt.txt` などで画像生成 → `01.png` として保存
- [ ] 本文の IMG 位置に添付
- [ ] `thumb_prompt.txt` でサムネ生成 → note の見出し画像に設定

## 3. リンク
- [ ] ハブURLが本文にある: https://preeminent-frangipane-e8530c.netlify.app/hub.html
- [ ] スマホでリンクを一度開く

## 4. 公開
- [ ] 無料公開
- [ ] マガジン「同人の選び方」に追加（任意）

## 半自動投稿
```powershell
python automation\note_publish.py --package "/home/runner/work/fanza-affiliate-kit/fanza-affiliate-kit/automation/out/2026-08-04_gap-when" --headed
```

生成モード: template
