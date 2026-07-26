#!/usr/bin/env python3
"""Copy site/ into campaigns/first/deploy_folder and rebuild zip."""
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "campaigns" / "first" / "deploy_folder"
ZIP = ROOT / "campaigns" / "first" / "doujin-lab-site.zip"

FILES = [
    "index.html",
    "hub.html",
    "review-a.html",
    "review-b.html",
    "review-c.html",
    "css/style.css",
    "js/age-gate.js",
    "robots.txt",
    "sitemap.xml",
]


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    for rel in FILES:
        src = SITE.joinpath(*rel.split("/"))
        if not src.is_file():
            raise SystemExit(f"missing {src}")
        dest = OUT.joinpath(*rel.split("/"))
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in FILES:
            z.write(SITE.joinpath(*rel.split("/")), rel)
    print("deploy_folder:", OUT)
    print("zip:", ZIP)
    print("files:", len(FILES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
