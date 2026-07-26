from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    return s[:60] or "note"


def build_package(
    *,
    out_root: Path,
    item: dict[str, Any],
    markdown: str,
    mode: str,
    image_dirs: dict[str, Any],
    settings: dict[str, Any],
) -> Path:
    day = date.today().isoformat()
    slug = item.get("slug") or slugify(item.get("title") or "post")
    pkg = out_root / f"{day}_{slug}"
    img_dir = pkg / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    (pkg / "article.md").write_text(markdown, encoding="utf-8")

    title = "同人メモ"
    for line in markdown.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    meta = {
        "date": day,
        "slug": slug,
        "title": title,
        "hub_url": settings.get("hub_url"),
        "generator_mode": mode,
        "series_item": item,
        "images": image_dirs.get("images") or [],
        "thumbnail_prompt": image_dirs.get("thumbnail"),
        "tags": ["同人", "FANZA", "比較", "選び方"],
    }
    (pkg / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    for i, prompt in enumerate(image_dirs.get("images") or [], start=1):
        (img_dir / f"{i:02d}_prompt.txt").write_text(prompt + "\n", encoding="utf-8")
        # placeholder so folder is non-empty for attach workflows
        (img_dir / f"{i:02d}_PLACEHOLDER.txt").write_text(
            "Generate image from sibling *_prompt.txt then save as "
            f"{i:02d}.png and attach in note at IMG slot {i}.\n",
            encoding="utf-8",
        )

    thumb_p = image_dirs.get("thumbnail") or "サムネ"
    (img_dir / "thumb_prompt.txt").write_text(thumb_p + "\n", encoding="utf-8")
    (img_dir / "thumb_PLACEHOLDER.txt").write_text(
        "Generate thumbnail PNG from thumb_prompt.txt → save as thumb.png\n"
        "Upload as note cover/thumbnail.\n",
        encoding="utf-8",
    )

    publish = f"""# 投稿チェックリスト（{day}）

## 1. 本文
- [ ] `article.md` を note 新規投稿に貼る
- [ ] タイトル: {title}

## 2. 画像
- [ ] `images/01_prompt.txt` などで画像生成 → `01.png` として保存
- [ ] 本文の IMG 位置に添付
- [ ] `thumb_prompt.txt` でサムネ生成 → note の見出し画像に設定

## 3. リンク
- [ ] ハブURLが本文にある: {settings.get('hub_url')}
- [ ] スマホでリンクを一度開く

## 4. 公開
- [ ] 無料公開
- [ ] マガジン「同人の選び方」に追加（任意）

## 半自動投稿
```powershell
python automation\\note_publish.py --package "{pkg}" --headed
```

生成モード: {mode}
"""
    (pkg / "PUBLISH.md").write_text(publish, encoding="utf-8")
    return pkg
