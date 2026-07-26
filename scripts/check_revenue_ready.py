#!/usr/bin/env python3
"""
Revenue-readiness structural checks for the live-oriented site kit.

Asserts:
- no noindex on HTML
- robots.txt + sitemap.xml present with expected URLs
- sticky CTA + affiliate id on hub
- age-gate script present
- diagnosis + note growth pack docs present

Exit 0 on full pass.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
CAMPAIGN = ROOT / "campaigns" / "first"


def main() -> int:
    errors: list[str] = []
    notes: list[str] = []

    htmls = list(SITE.glob("*.html"))
    if not htmls:
        errors.append("no HTML in site/")

    for p in htmls:
        t = p.read_text(encoding="utf-8")
        if "noindex" in t:
            errors.append(f"{p.name} still has noindex")
        if 'content="index,follow"' not in t and p.name != "missing":
            # allow if robots elsewhere; prefer explicit
            if 'name="robots"' not in t:
                errors.append(f"{p.name} missing robots meta")
        if p.name in ("hub.html", "review-a.html", "review-b.html", "review-c.html"):
            if "fireworker-003" not in t:
                errors.append(f"{p.name} missing affiliate id")
            if "al.fanza.co.jp" not in t:
                errors.append(f"{p.name} missing aff host")
            if "age-gate.js" not in t:
                errors.append(f"{p.name} missing age-gate.js")
            if "sticky-cta" not in t and p.name != "index.html":
                errors.append(f"{p.name} missing sticky-cta")

    hub = (SITE / "hub.html").read_text(encoding="utf-8")
    if "sticky-cta" not in hub:
        errors.append("hub missing sticky-cta")
    if "canonical" not in hub:
        errors.append("hub missing canonical")

    robots = SITE / "robots.txt"
    if not robots.is_file():
        errors.append("robots.txt missing")
    else:
        rt = robots.read_text(encoding="utf-8")
        if "Sitemap:" not in rt:
            errors.append("robots.txt missing Sitemap")
        if "Allow: /" not in rt:
            errors.append("robots.txt should Allow: /")

    sm = SITE / "sitemap.xml"
    if not sm.is_file():
        errors.append("sitemap.xml missing")
    else:
        st = sm.read_text(encoding="utf-8")
        for path in ("hub.html", "review-a.html", "review-b.html", "review-c.html"):
            if path not in st:
                errors.append(f"sitemap missing {path}")

    age = SITE / "js" / "age-gate.js"
    if not age.is_file():
        errors.append("js/age-gate.js missing")
    else:
        at = age.read_text(encoding="utf-8")
        if "doujin_lab_age_ok" not in at:
            errors.append("age-gate missing storage key")
        if "position:fixed" not in at and "position: fixed" not in at:
            # inline style uses position:fixed without space after colon sometimes
            if "position:fixed" not in at.replace(" ", ""):
                errors.append("age-gate should force fixed overlay")

    for rel in (
        "11_ZERO_CLICK_DIAGNOSIS.md",
        "12_NOTE_GROWTH_PACK.md",
        "13_DEPLOY_AND_SELFTEST.md",
    ):
        if not (CAMPAIGN / rel).is_file():
            # 13 may be written after; soft for now only if missing after create
            if rel.startswith("13") and not (CAMPAIGN / rel).is_file():
                notes.append(f"pending {rel}")
            else:
                errors.append(f"missing {rel}")

    css = (SITE / "css" / "style.css").read_text(encoding="utf-8")
    if ".sticky-cta" not in css:
        errors.append("css missing .sticky-cta")

    report = {
        "ok": len(errors) == 0,
        "errors": errors,
        "notes": notes,
        "html_count": len(htmls),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS - revenue readiness structure OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
