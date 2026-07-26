#!/usr/bin/env python3
"""
FANZA affiliate kit inventory checker.

Reads sections.json next to the kit root, verifies each required section file
exists and contains the required markers. Exit 0 on full pass, 1 on any failure.

Usage:
  python scripts/check_kit.py
  python scripts/check_kit.py --json
  python scripts/check_kit.py --root /path/to/fanza_affiliate_kit
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_SECTION_IDS = (
    "runbook",
    "market_research_funnel",
    "environment_links",
    "article_template",
    "text_click_method",
    "video_click_method",
)


def kit_root_from(start: Path | None = None) -> Path:
    """Resolve kit root (directory containing sections.json)."""
    if start is not None:
        root = start.resolve()
        if (root / "sections.json").is_file():
            return root
        raise FileNotFoundError(f"sections.json not found under --root {root}")

    # scripts/check_kit.py -> kit root is parent of scripts/
    here = Path(__file__).resolve().parent
    candidate = here.parent
    if (candidate / "sections.json").is_file():
        return candidate
    raise FileNotFoundError(
        f"sections.json not found. Looked at {candidate / 'sections.json'}"
    )


def load_sections(root: Path) -> dict[str, Any]:
    path = root / "sections.json"
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if "required_sections" not in data or not isinstance(data["required_sections"], list):
        raise ValueError("sections.json missing required_sections list")
    return data


def check_section(root: Path, section: dict[str, Any]) -> dict[str, Any]:
    sid = section.get("id", "<missing-id>")
    rel = section.get("path", "")
    must = section.get("must_contain") or []
    result: dict[str, Any] = {
        "id": sid,
        "path": rel,
        "exists": False,
        "missing_markers": [],
        "ok": False,
    }
    if not rel:
        result["missing_markers"] = ["<no path in sections.json>"]
        return result

    file_path = root / rel
    if not file_path.is_file():
        result["missing_markers"] = [f"FILE_MISSING: {rel}"]
        return result

    result["exists"] = True
    text = file_path.read_text(encoding="utf-8")
    missing = [m for m in must if m not in text]
    result["missing_markers"] = missing
    result["ok"] = len(missing) == 0
    return result


def run_checks(root: Path) -> dict[str, Any]:
    data = load_sections(root)
    sections = data["required_sections"]
    results = [check_section(root, s) for s in sections]
    by_id = {r["id"]: r for r in results}

    missing_ids = [sid for sid in REQUIRED_SECTION_IDS if sid not in by_id]
    extra_fail = [r for r in results if not r["ok"]]

    all_ok = not missing_ids and all(r["ok"] for r in results)
    return {
        "kit_root": str(root),
        "kit_name": data.get("kit_name"),
        "version": data.get("version"),
        "all_ok": all_ok,
        "required_core_ids": list(REQUIRED_SECTION_IDS),
        "missing_core_ids": missing_ids,
        "sections": results,
        "failed_count": len(extra_fail) + len(missing_ids),
    }


def format_report(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("=== FANZA Affiliate Kit Checker ===")
    lines.append(f"root: {report['kit_root']}")
    lines.append(f"kit:  {report.get('kit_name')} v{report.get('version')}")
    lines.append("")
    for r in report["sections"]:
        status = "PASS" if r["ok"] else "FAIL"
        lines.append(f"[{status}] {r['id']}  ({r['path']})")
        if not r["ok"]:
            for m in r["missing_markers"]:
                lines.append(f"       - missing: {m}")
    if report["missing_core_ids"]:
        lines.append("")
        lines.append("Missing core section IDs in sections.json:")
        for sid in report["missing_core_ids"]:
            lines.append(f"  - {sid}")
    lines.append("")
    if report["all_ok"]:
        lines.append("RESULT: PASS - all required sections present.")
    else:
        lines.append(
            f"RESULT: FAIL - {report['failed_count']} problem(s). "
            "See missing markers above."
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check FANZA affiliate kit inventory")
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Kit root directory (contains sections.json)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON report",
    )
    args = parser.parse_args(argv)

    try:
        root = kit_root_from(args.root)
        report = run_checks(root)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(format_report(report), end="")

    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
