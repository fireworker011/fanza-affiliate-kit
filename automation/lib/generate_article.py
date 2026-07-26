from __future__ import annotations

import os
import re
from typing import Any


def _product_by_id(settings: dict[str, Any], pid: str | None) -> dict[str, Any] | None:
    if not pid:
        return None
    for p in settings.get("products") or []:
        if p.get("id") == pid:
            return p
    return None


def generate_template_article(
    *,
    item: dict[str, Any],
    settings: dict[str, Any],
    project_prompt: str,
    materials_excerpt: str,
) -> str:
    """Offline generator (no API). Uses series item + products + rules."""
    hub = settings["hub_url"]
    site = settings.get("site_base", "").rstrip("/")
    focus = _product_by_id(settings, item.get("focus_product"))
    products = settings.get("products") or []

    lines: list[str] = []
    title = item.get("title") or "同人の選び方メモ"
    lines.append(f"# {title}")
    lines.append("")
    lines.append("<!-- THUMB: 暗い背景に「欲求の型で選ぶ」白い太字、成人向け同人比較のサムネ、文字多め禁止、シンプル -->")
    lines.append("")
    lines.append(
        f"テーマ: {item.get('angle', '')}。"
        "ランキング任せの失敗を減らし、自分の回路に合う一冊へ寄せるメモです。"
    )
    lines.append("")
    lines.append("<!-- IMG: ノートとチェックリストのフラットイラスト、机の上、落ち着いた色 -->")
    lines.append("")
    lines.append("## 先に結論")
    lines.append("")
    lines.append("| 欲しいもの | 型 |")
    lines.append("|------------|-----|")
    lines.append("| 甘さ・安心 | SWEET（入口） |")
    lines.append("| 印象の変化 | GAP |")
    lines.append("| 長尺・禁断シチュ | VOLUME+TABOO（目的買い） |")
    lines.append("")
    lines.append("大事なのは「どれが一番エロいか」ではなく、**どれが今の自分に刺さるか**です。")
    lines.append("")

    if focus:
        lines.append(f"## 今日フォーカス: {focus.get('name')}")
        lines.append("")
        lines.append(
            f"サークル: {focus.get('circle')} / 品番: {focus.get('cid')} / ラベル: {focus.get('label')}"
        )
        lines.append("")
        lines.append(
            f"向き: {item.get('angle')}。"
            "苦手タグがあるなら公式で確認してから。合わなければスキップで問題ありません。"
        )
        lines.append("")
        lines.append("<!-- IMG: 抽象的な分岐矢印（A/B/C）、R18直球描写なし -->")
        lines.append("")
        rev = focus.get("review_path") or ""
        if site and rev:
            lines.append(f"個別の向き不向き: {site}{rev}")
            lines.append("")
    else:
        lines.append("## 3作品の位置づけ（短縮）")
        lines.append("")
        for p in products:
            lines.append(
                f"- **{p.get('label')}** … {p.get('name')}（{p.get('cid')}）"
            )
        lines.append("")
        lines.append("<!-- IMG: 3つのカードが並ぶ図、あまあま・ギャップ・長尺のラベル -->")
        lines.append("")

    lines.append("## 30秒チェック")
    lines.append("")
    lines.append("1. クセを抑えめに甘く入りたい → SWEET")
    lines.append("2. 別人化ギャップが欲しい → GAP")
    lines.append("3. 尺とシチュで沈みたい → 長尺（タグ自己チェック必須）")
    lines.append("")
    lines.append("迷ったら入口はSWEETからで十分です。")
    lines.append("")
    lines.append("## 詳細・診断はこちら")
    lines.append("")
    lines.append("比較表と簡単な診断はハブにまとめています。")
    lines.append("")
    lines.append(hub)
    lines.append("")
    lines.append("- 年齢確認あり（成人向け）")
    lines.append("- ページ内にアフィリエイトリンクを含みます")
    lines.append("- 価格・評価・タグは公式の最新表示を正としてください")
    lines.append("")
    lines.append("## 免責")
    lines.append("")
    lines.append("- 18歳未満はご覧にならないでください")
    lines.append("- 紹介にはアフィリエイトが含まれる場合があります")
    lines.append("- 未読の断定的な体験談は書いていません")
    lines.append("")
    # keep prompt/materials referenced lightly for traceability (not dumped fully)
    lines.append("<!-- generator: template; project_prompt_chars=%d materials_chars=%d -->" % (
        len(project_prompt),
        len(materials_excerpt),
    ))
    lines.append("")
    return "\n".join(lines)


def generate_with_xai_if_available(
    *,
    item: dict[str, Any],
    settings: dict[str, Any],
    project_prompt: str,
    materials_excerpt: str,
) -> tuple[str, str]:
    """Returns (markdown, mode) where mode is 'xai' or 'template'."""
    api_key = os.environ.get("XAI_API_KEY") or os.environ.get("xai_api_key")
    if not api_key:
        return (
            generate_template_article(
                item=item,
                settings=settings,
                project_prompt=project_prompt,
                materials_excerpt=materials_excerpt,
            ),
            "template",
        )

    try:
        import urllib.request
        import json

        hub = settings["hub_url"]
        user = (
            f"シリーズ題材: {json.dumps(item, ensure_ascii=False)}\n"
            f"ハブURL必須: {hub}\n"
            f"商品マスタ: {json.dumps(settings.get('products'), ensure_ascii=False)}\n"
            f"素材抜粋:\n{materials_excerpt[:8000]}\n"
            "Markdown本文のみ出力。"
        )
        body = {
            "model": os.environ.get("XAI_MODEL", "grok-3"),
            "messages": [
                {"role": "system", "content": project_prompt},
                {"role": "user", "content": user},
            ],
            "temperature": 0.7,
        }
        req = urllib.request.Request(
            "https://api.x.ai/v1/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = data["choices"][0]["message"]["content"]
        if not text.strip().startswith("#"):
            text = f"# {item.get('title', '同人メモ')}\n\n" + text
        if hub not in text:
            text += f"\n\n詳細・診断: {hub}\n"
        return text, "xai"
    except Exception:
        return (
            generate_template_article(
                item=item,
                settings=settings,
                project_prompt=project_prompt,
                materials_excerpt=materials_excerpt,
            ),
            "template_fallback",
        )


IMG_RE = re.compile(r"<!--\s*IMG:\s*(.+?)\s*-->", re.I)
THUMB_RE = re.compile(r"<!--\s*THUMB:\s*(.+?)\s*-->", re.I)


def extract_image_directives(markdown: str) -> dict[str, Any]:
    imgs = [m.group(1).strip() for m in IMG_RE.finditer(markdown)]
    thumbs = [m.group(1).strip() for m in THUMB_RE.finditer(markdown)]
    return {
        "images": imgs,
        "thumbnail": thumbs[0] if thumbs else "暗い背景、欲求の型、比較、シンプル文字サムネ",
    }
