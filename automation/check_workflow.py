#!/usr/bin/env python3
"""Structural check for cloud daily workflow (no network)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WF = ROOT / ".github" / "workflows" / "daily_note_package.yml"


def main() -> int:
    if not WF.is_file():
        print("FAIL: workflow missing", WF)
        return 1
    text = WF.read_text(encoding="utf-8")
    required = [
        "schedule:",
        "cron:",
        "workflow_dispatch",
        "actions/checkout@v4",
        "automation/run_daily.py",
        "upload-artifact@v4",
        "git push",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        print("FAIL missing:", missing)
        return 1
    # ensure not only windows-task
    if "runs-on: ubuntu-latest" not in text:
        print("FAIL: expected ubuntu-latest runner (cloud)")
        return 1
    print("OK workflow present and looks cloud-scheduled")
    print(f"path: {WF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
