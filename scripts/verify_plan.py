#!/usr/bin/env python3
"""
Execute the plan's Verification plan against the shipped kit.
Drives check_kit.main / run_checks (real path) and structural file checks.
Exit 0 only if all gating + evidence checks pass.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
KIT_ROOT = SCRIPTS.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_kit  # shipped entry


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def verify(scratch: Path | None = None) -> tuple[bool, str]:
    errors: list[str] = []
    lines: list[str] = []
    lines.append("=== Plan Verification Report ===")
    lines.append(f"kit_root: {KIT_ROOT}")
    lines.append("")

    # --- V1: inventory checker real entry path ---
    lines.append("## V1 inventory checker (gating)")
    code = check_kit.main([])
    report = check_kit.run_checks(KIT_ROOT)
    text = check_kit.format_report(report)
    lines.append(text.rstrip())
    if code != 0 or not report["all_ok"]:
        fail(f"V1: checker exit={code} all_ok={report['all_ok']}", errors)
    core = {
        "runbook",
        "article_template",
        "market_research_funnel",
        "environment_links",
        "text_click_method",
        "video_click_method",
    }
    present = {s["id"] for s in report["sections"] if s["ok"]}
    missing_core = core - present
    if missing_core:
        fail(f"V1: missing core IDs {sorted(missing_core)}", errors)
    else:
        lines.append(f"core IDs all present: {sorted(core)}")
    if scratch:
        (scratch / "kit_check.log").write_text(
            text + f"exit_code={code}\n", encoding="utf-8"
        )
    lines.append("")

    # --- V2: runbook ordered steps ---
    lines.append("## V2 runbook ordered steps (gating)")
    runbook = (KIT_ROOT / "docs" / "01_runbook.md").read_text(encoding="utf-8")
    step_markers = [
        ("market research", "## STEP 1"),
        ("environment", "## STEP 2"),
        ("content structure", "## STEP 3"),
        ("affiliate register/links", "## STEP 4"),
        ("earnings structure", "## STEP 5"),
        ("text+video click methods", "## STEP 6"),
        ("publish/improve", "## STEP 7"),
    ]
    positions = []
    for name, marker in step_markers:
        pos = runbook.find(marker)
        if pos < 0:
            fail(f"V2: missing {marker} ({name})", errors)
            lines.append(f"  MISS {marker}")
        else:
            positions.append(pos)
            # each step needs Done when nearby
            chunk = runbook[pos : pos + 2500]
            if "Done when" not in chunk:
                fail(f"V2: {marker} lacks Done when nearby", errors)
                lines.append(f"  WEAK {marker} (no Done when)")
            else:
                lines.append(f"  OK   {marker} ({name}) + Done when")
    if positions != sorted(positions):
        fail("V2: STEP markers not in ascending order", errors)
    # actionable bullets
    if runbook.count("- [ ]") < 10:
        fail("V2: expected multiple actionable checkboxes in runbook", errors)
    else:
        lines.append(f"  OK   actionable checkboxes count={runbook.count('- [ ]')}")
    lines.append("")

    # --- V3: article template + market research ---
    lines.append("## V3 article template + market research (gating)")
    article = (KIT_ROOT / "templates" / "fanza_article_template.md").read_text(
        encoding="utf-8"
    )
    for slot in ("{{タイトル}}", "{{ターゲットキーワード}}", "CTA-1", "CTA-2", "CTA-3"):
        if slot not in article:
            fail(f"V3: article template missing {slot}", errors)
            lines.append(f"  MISS {slot}")
        else:
            lines.append(f"  OK   {slot}")
    research = (KIT_ROOT / "docs" / "02_market_research_funnel.md").read_text(
        encoding="utf-8"
    )
    for marker in (
        "## ニッチ選定",
        "## キーワード・需要チェック",
        "## 稼ぎ直結コンテンツマップ",
        "affiliate CTA",
    ):
        if marker not in research:
            fail(f"V3: research/funnel missing {marker!r}", errors)
            lines.append(f"  MISS {marker}")
        else:
            lines.append(f"  OK   {marker}")
    lines.append("")

    # --- V4: official URLs / tools + region caveat ---
    lines.append("## V4 official references (evidence)")
    env = (KIT_ROOT / "docs" / "03_environment_and_links.md").read_text(
        encoding="utf-8"
    )
    readme = (KIT_ROOT / "README.md").read_text(encoding="utf-8")
    blob = env + "\n" + runbook + "\n" + readme
    for ref in (
        "affiliate.dmm.com",
        "ツールバー",
        "fee/rate",
        "support.dmm.com/affiliate",
    ):
        if ref not in blob:
            fail(f"V4: missing official ref {ref!r}", errors)
            lines.append(f"  MISS {ref}")
        else:
            lines.append(f"  OK   {ref}")
    if "地域" not in blob and "region" not in blob.lower():
        fail("V4: missing region-block caveat", errors)
        lines.append("  MISS region-block caveat")
    else:
        lines.append("  OK   region-block caveat present")
    lines.append("")

    # --- V5: rerun checker non-flaky ---
    lines.append("## V5 inventory checker rerun (evidence)")
    code2 = check_kit.main([])
    report2 = check_kit.run_checks(KIT_ROOT)
    text2 = check_kit.format_report(report2)
    lines.append(text2.rstrip())
    if code2 != 0 or not report2["all_ok"]:
        fail(f"V5: rerun exit={code2} all_ok={report2['all_ok']}", errors)
    if report2["all_ok"] != report["all_ok"]:
        fail("V5: flaky result between runs", errors)
    else:
        lines.append("  OK   non-flaky (same all_ok=True)")
    if scratch:
        (scratch / "kit_check_rerun.log").write_text(
            text2 + f"exit_code={code2}\n", encoding="utf-8"
        )
    lines.append("")

    ok = len(errors) == 0
    lines.append("## SUMMARY")
    if ok:
        lines.append("RESULT: PASS - all verification plan observations hold.")
    else:
        lines.append(f"RESULT: FAIL - {len(errors)} issue(s):")
        for e in errors:
            lines.append(f"  - {e}")
    body = "\n".join(lines) + "\n"
    if scratch:
        (scratch / "verify_plan.log").write_text(body, encoding="utf-8")
        (scratch / "verify_plan.json").write_text(
            json.dumps(
                {
                    "ok": ok,
                    "errors": errors,
                    "core_present": sorted(present),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    return ok, body


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument(
        "--scratch",
        type=Path,
        default=None,
        help="Directory to write kit_check.log, kit_check_rerun.log, verify_plan.log",
    )
    args = p.parse_args(argv)
    scratch = args.scratch
    if scratch:
        scratch.mkdir(parents=True, exist_ok=True)
    ok, body = verify(scratch)
    print(body, end="")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
