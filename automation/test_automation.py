#!/usr/bin/env python3
"""Tests drive real run_daily and generators."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

AUTO = Path(__file__).resolve().parent
KIT = AUTO.parent
if str(AUTO) not in sys.path:
    sys.path.insert(0, str(AUTO))

from lib.generate_article import (  # noqa: E402
    extract_image_directives,
    generate_template_article,
)
from lib.package_builder import build_package  # noqa: E402
from lib.state import pick_series_item  # noqa: E402


class TestAutomation(unittest.TestCase):
    def test_template_contains_hub_and_img_slots(self):
        settings = json.loads(
            (AUTO / "config" / "settings.json").read_text(encoding="utf-8")
        )
        series = json.loads(
            (AUTO / "config" / "series.json").read_text(encoding="utf-8")
        )
        item = series["queue"][0]
        md = generate_template_article(
            item=item,
            settings=settings,
            project_prompt="rules",
            materials_excerpt="mat",
        )
        self.assertIn(settings["hub_url"], md)
        self.assertIn("# ", md)
        dirs = extract_image_directives(md)
        self.assertGreaterEqual(len(dirs["images"]), 1)
        self.assertTrue(dirs["thumbnail"])

    def test_pick_series_advances(self):
        series = {"queue": [{"slug": "a"}, {"slug": "b"}]}
        item1, st1 = pick_series_item(series, {"next_index": 0})
        item2, st2 = pick_series_item(series, st1)
        self.assertEqual(item1["slug"], "a")
        self.assertEqual(item2["slug"], "b")
        self.assertEqual(st2["next_index"], 0)

    def test_build_package_files(self):
        settings = json.loads(
            (AUTO / "config" / "settings.json").read_text(encoding="utf-8")
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            item = {"slug": "t", "title": "テスト記事"}
            md = "# テスト記事\n\n<!-- THUMB: t -->\n<!-- IMG: i1 -->\n" + settings["hub_url"]
            pkg = build_package(
                out_root=out,
                item=item,
                markdown=md,
                mode="template",
                image_dirs=extract_image_directives(md),
                settings=settings,
            )
            self.assertTrue((pkg / "article.md").is_file())
            self.assertTrue((pkg / "meta.json").is_file())
            self.assertTrue((pkg / "PUBLISH.md").is_file())
            self.assertTrue((pkg / "images" / "01_prompt.txt").is_file())
            self.assertTrue((pkg / "images" / "thumb_prompt.txt").is_file())
            body = (pkg / "article.md").read_text(encoding="utf-8")
            self.assertIn(settings["hub_url"], body)

    def test_run_daily_cli(self):
        proc = subprocess.run(
            [sys.executable, str(AUTO / "run_daily.py"), "--dry-run"],
            cwd=str(KIT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("OK package:", proc.stdout)
        self.assertIn("mode:", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
