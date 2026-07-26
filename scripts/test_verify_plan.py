#!/usr/bin/env python3
"""Drive real verify_plan.verify against the shipped kit."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import verify_plan  # noqa: E402 — shipped module


class TestVerifyPlan(unittest.TestCase):
    def test_verify_passes_on_real_kit(self):
        ok, body = verify_plan.verify(scratch=None)
        self.assertTrue(ok, msg=body)
        self.assertIn("RESULT: PASS", body)
        self.assertIn("V1", body)
        self.assertIn("V5", body)

    def test_verify_writes_scratch_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            scratch = Path(tmp)
            ok, _ = verify_plan.verify(scratch=scratch)
            self.assertTrue(ok)
            self.assertTrue((scratch / "kit_check.log").is_file())
            self.assertTrue((scratch / "kit_check_rerun.log").is_file())
            self.assertTrue((scratch / "verify_plan.log").is_file())
            log = (scratch / "verify_plan.log").read_text(encoding="utf-8")
            self.assertIn("RESULT: PASS", log)

    def test_main_exit_zero(self):
        self.assertEqual(verify_plan.main([]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
