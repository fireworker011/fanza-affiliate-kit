#!/usr/bin/env python3
"""
Semi-automated note.com publisher (unofficial, best-effort).

Requires:
  pip install playwright
  playwright install chromium

First run with --headed and log in to note.com manually.
Profile is stored under automation/.browser_profile/

This does NOT drive grok.com projects (no public API).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

AUTO = Path(__file__).resolve().parent
PROFILE = AUTO / ".browser_profile"


def load_package(pkg: Path) -> tuple[str, str]:
    article = (pkg / "article.md").read_text(encoding="utf-8")
    title = "同人メモ"
    for line in article.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    # strip HTML comments for paste cleanliness
    import re

    body = re.sub(r"<!--.*?-->", "", article, flags=re.S).strip()
    # remove leading title line from body (note has separate title field)
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        body = "\n".join(lines[1:]).strip()
    return title, body


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--headed", action="store_true", default=True)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument(
        "--draft-only",
        action="store_true",
        help="Stop after filling editor (do not click publish)",
    )
    args = parser.parse_args(argv)
    headed = not args.headless

    pkg = args.package.resolve()
    if not (pkg / "article.md").is_file():
        print(f"ERROR: article.md missing in {pkg}", file=sys.stderr)
        return 1

    title, body = load_package(pkg)
    meta_path = pkg / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Playwright not installed.\n"
            "  pip install playwright\n"
            "  playwright install chromium\n"
            "Falling back: package is ready for manual paste.\n"
            f"  title: {title}\n"
            f"  body chars: {len(body)}\n"
            f"  see: {pkg / 'PUBLISH.md'}",
            file=sys.stderr,
        )
        return 2

    PROFILE.mkdir(parents=True, exist_ok=True)
    print("Launching Chromium with persistent profile:", PROFILE)
    print("If not logged in, log in to note.com in the opened window.")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE),
            headless=not headed,
            locale="ja-JP",
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://note.com/notes/new", wait_until="domcontentloaded")
        time.sleep(2)

        # Best-effort selectors (note UI changes often)
        filled = False
        for sel in [
            'textarea[placeholder*="タイトル"]',
            'input[placeholder*="タイトル"]',
            '[data-testid="note-title"]',
            "textarea",
        ]:
            try:
                loc = page.locator(sel).first
                if loc.count() and loc.is_visible(timeout=1500):
                    loc.fill(title)
                    filled = True
                    break
            except Exception:
                continue

        # body: contenteditable
        body_ok = False
        for sel in [
            '[contenteditable="true"]',
            ".ProseMirror",
            "div[role='textbox']",
        ]:
            try:
                loc = page.locator(sel).first
                if loc.count():
                    loc.click()
                    page.keyboard.type(body[:5000], delay=0)  # long body may need paste
                    # prefer clipboard paste for full body
                    page.evaluate(
                        """async (text) => {
                          await navigator.clipboard.writeText(text);
                        }""",
                        body,
                    )
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Control+V")
                    body_ok = True
                    break
            except Exception:
                continue

        print(f"title_filled={filled} body_attempt={body_ok}")
        print("Images/thumbnail must be attached manually (file picker varies).")
        print(f"Image folder: {pkg / 'images'}")
        print(f"meta tags: {meta.get('tags')}")

        if args.draft_only or not filled:
            print("Stopping before publish (draft-only or selectors failed).")
            print("Complete in browser, then close window.")
            if headed:
                page.wait_for_timeout(600_000)
            context.close()
            return 0 if filled else 3

        # Do not auto-click Publish by default — too risky
        print(
            "Safety: auto-publish click is disabled. "
            "Review the draft in browser and press 公開 yourself."
        )
        if headed:
            page.wait_for_timeout(600_000)
        context.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
