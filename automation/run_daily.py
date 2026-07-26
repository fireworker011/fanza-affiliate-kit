#!/usr/bin/env python3
"""
Daily pipeline: materials + series queue -> article package for note.

Usage:
  python automation/run_daily.py
  python automation/run_daily.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# allow running as script
AUTO = Path(__file__).resolve().parent
KIT = AUTO.parent
if str(AUTO) not in sys.path:
    sys.path.insert(0, str(AUTO))

from lib.generate_article import (  # noqa: E402
    extract_image_directives,
    generate_with_xai_if_available,
)
from lib.materials import load_materials  # noqa: E402
from lib.package_builder import build_package  # noqa: E402
from lib.paths import (  # noqa: E402
    DEFAULT_PROMPT,
    DEFAULT_SERIES,
    DEFAULT_SETTINGS,
    KIT_ROOT,
)
from lib.state import load_state, pick_series_item, save_state  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build daily note affiliate package")
    parser.add_argument("--dry-run", action="store_true", help="Do not advance state")
    parser.add_argument("--settings", type=Path, default=DEFAULT_SETTINGS)
    args = parser.parse_args(argv)

    settings = json.loads(args.settings.read_text(encoding="utf-8"))
    series = json.loads(DEFAULT_SERIES.read_text(encoding="utf-8"))
    project_prompt = DEFAULT_PROMPT.read_text(encoding="utf-8")

    state_path = KIT_ROOT / settings.get("state_file", "automation/state.json")
    state = load_state(state_path)
    item, new_state = pick_series_item(series, state)

    materials = load_materials(KIT_ROOT, settings.get("materials_glob") or [])
    md, mode = generate_with_xai_if_available(
        item=item,
        settings=settings,
        project_prompt=project_prompt,
        materials_excerpt=materials,
    )
    dirs = extract_image_directives(md)

    out_root = KIT_ROOT / settings.get("output_dir", "automation/out")
    pkg = build_package(
        out_root=out_root,
        item=item,
        markdown=md,
        mode=mode,
        image_dirs=dirs,
        settings=settings,
    )

    if not args.dry_run:
        save_state(state_path, new_state)

    print(f"OK package: {pkg}")
    print(f"mode: {mode}")
    print(f"title: {item.get('title')}")
    print(f"images: {len(dirs.get('images') or [])}")
    print(f"hub: {settings.get('hub_url')}")
    print(f"next: open {pkg / 'PUBLISH.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
