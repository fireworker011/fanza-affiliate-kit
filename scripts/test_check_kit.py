#!/usr/bin/env python3
"""
Tests that drive the real check_kit entry points (not re-implemented logic).
Run from kit root or scripts/:
  python scripts/test_check_kit.py
  python -m pytest scripts/test_check_kit.py -q
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure scripts dir is importable
SCRIPTS = Path(__file__).resolve().parent
KIT_ROOT = SCRIPTS.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_kit  # noqa: E402  — shipped module under test


class TestCheckKitRealPath(unittest.TestCase):
    def test_kit_root_resolves_to_real_kit(self):
        root = check_kit.kit_root_from(None)
        self.assertEqual(root, KIT_ROOT.resolve())
        self.assertTrue((root / "sections.json").is_file())

    def test_run_checks_on_real_kit_passes(self):
        report = check_kit.run_checks(KIT_ROOT.resolve())
        self.assertTrue(
            report["all_ok"],
            msg=f"Expected real kit to pass, got: {check_kit.format_report(report)}",
        )
        for sid in check_kit.REQUIRED_SECTION_IDS:
            self.assertIn(sid, {s["id"] for s in report["sections"]})
            section = next(s for s in report["sections"] if s["id"] == sid)
            self.assertTrue(section["ok"], msg=f"{sid} failed: {section}")

    def test_main_exit_code_zero_on_real_kit(self):
        code = check_kit.main([])
        self.assertEqual(code, 0)

    def test_main_json_flag_emits_all_ok(self):
        # Capture via subprocess to exercise CLI entry exactly as users run it
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "check_kit.py"), "--json"],
            cwd=str(KIT_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        data = json.loads(proc.stdout)
        self.assertTrue(data["all_ok"])
        ids = {s["id"] for s in data["sections"]}
        for sid in check_kit.REQUIRED_SECTION_IDS:
            self.assertIn(sid, ids)

    def test_missing_file_fails_loud(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Minimal broken sections.json pointing at missing file
            (tmp_path / "sections.json").write_text(
                json.dumps(
                    {
                        "kit_name": "broken",
                        "version": "0",
                        "required_sections": [
                            {
                                "id": "runbook",
                                "path": "nope.md",
                                "must_contain": ["## STEP 1"],
                            },
                            {
                                "id": "market_research_funnel",
                                "path": "nope2.md",
                                "must_contain": ["## ニッチ選定"],
                            },
                            {
                                "id": "environment_links",
                                "path": "nope3.md",
                                "must_contain": ["affiliate.dmm.com"],
                            },
                            {
                                "id": "article_template",
                                "path": "nope4.md",
                                "must_contain": ["CTA-1"],
                            },
                            {
                                "id": "text_click_method",
                                "path": "nope5.md",
                                "must_contain": ["## CTA文言パターン"],
                            },
                            {
                                "id": "video_click_method",
                                "path": "nope6.md",
                                "must_contain": ["## 動画導線"],
                            },
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            report = check_kit.run_checks(tmp_path)
            self.assertFalse(report["all_ok"])
            self.assertGreater(report["failed_count"], 0)
            code = check_kit.main(["--root", str(tmp_path)])
            self.assertEqual(code, 1)

    def test_missing_marker_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "docs").mkdir()
            # File exists but missing required markers
            (tmp_path / "docs" / "01_runbook.md").write_text(
                "# empty runbook without steps\n", encoding="utf-8"
            )
            sections = []
            for sid, path, markers in [
                ("runbook", "docs/01_runbook.md", ["## STEP 1", "Done when"]),
                ("market_research_funnel", "docs/m.md", ["## ニッチ選定"]),
                ("environment_links", "docs/e.md", ["affiliate.dmm.com"]),
                ("article_template", "docs/a.md", ["CTA-1"]),
                ("text_click_method", "docs/t.md", ["## CTA文言パターン"]),
                ("video_click_method", "docs/v.md", ["## 動画導線"]),
            ]:
                sections.append(
                    {"id": sid, "path": path, "must_contain": markers}
                )
            (tmp_path / "sections.json").write_text(
                json.dumps({"required_sections": sections}), encoding="utf-8"
            )
            report = check_kit.run_checks(tmp_path)
            self.assertFalse(report["all_ok"])
            runbook = next(s for s in report["sections"] if s["id"] == "runbook")
            self.assertTrue(runbook["exists"])
            self.assertIn("## STEP 1", runbook["missing_markers"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
