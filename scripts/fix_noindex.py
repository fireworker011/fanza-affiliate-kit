#!/usr/bin/env python3
"""Remove noindex from site HTML; ensure index,follow robots meta."""
from __future__ import annotations

from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
NEEDLE = '<meta name="robots" content="noindex,nofollow" />'
WANT = '<meta name="robots" content="index,follow" />'


def fix_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    original = text
    text = text.replace(NEEDLE, WANT)
    # if no robots meta at all, insert before stylesheet
    if 'name="robots"' not in text:
        text = text.replace(
            '<link rel="stylesheet"',
            f"  {WANT}\n  <link rel=\"stylesheet\"",
            1,
        )
    if text != original:
        path.write_text(text, encoding="utf-8")
        return "updated"
    return "unchanged"


def main() -> int:
    for p in sorted(SITE.glob("*.html")):
        print(f"{p.name}: {fix_file(p)}")
    left = [p.name for p in SITE.glob("*.html") if "noindex" in p.read_text(encoding="utf-8")]
    if left:
        print("FAIL still noindex:", left)
        return 1
    print("OK no noindex remaining")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
