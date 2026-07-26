from __future__ import annotations

from pathlib import Path

# automation/lib/paths.py -> kit root
KIT_ROOT = Path(__file__).resolve().parents[2]
AUTO_ROOT = KIT_ROOT / "automation"
CONFIG_DIR = AUTO_ROOT / "config"
DEFAULT_SETTINGS = CONFIG_DIR / "settings.json"
DEFAULT_SERIES = CONFIG_DIR / "series.json"
DEFAULT_PROMPT = CONFIG_DIR / "project_prompt.md"
