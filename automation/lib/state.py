from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_state(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"next_index": 0, "history": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def pick_series_item(series: dict[str, Any], state: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    queue = series.get("queue") or []
    if not queue:
        raise ValueError("series.json queue is empty")
    idx = int(state.get("next_index") or 0) % len(queue)
    item = queue[idx]
    state = dict(state)
    state["next_index"] = (idx + 1) % len(queue)
    history = list(state.get("history") or [])
    history.append({"slug": item.get("slug"), "index": idx})
    state["history"] = history[-50:]
    return item, state
