#!/usr/bin/env python3
"""Drive real check_revenue_ready / fix_noindex entry points."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_revenue_ready  # noqa: E402
import fix_noindex  # noqa: E402


class TestRevenueReady(unittest.TestCase):
    def test_fix_noindex_idempotent_on_site(self):
        # real entry: main() should report no noindex left
        code = fix_noindex.main()
        self.assertEqual(code, 0)
        for p in (ROOT / "site").glob("*.html"):
            self.assertNotIn("noindex", p.read_text(encoding="utf-8"), p.name)

    def test_check_revenue_ready_passes(self):
        code = check_revenue_ready.main()
        self.assertEqual(code, 0)

    def test_cli_subprocess(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "check_revenue_ready.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("RESULT: PASS", proc.stdout)

    def test_hub_has_sticky_and_aff(self):
        hub = (ROOT / "site" / "hub.html").read_text(encoding="utf-8")
        self.assertIn("sticky-cta", hub)
        self.assertIn("fireworker-003", hub)
        self.assertIn("index,follow", hub)
        self.assertNotIn("noindex", hub)


if __name__ == "__main__":
    unittest.main(verbosity=2)
