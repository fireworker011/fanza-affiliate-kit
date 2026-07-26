from __future__ import annotations

from pathlib import Path


def load_materials(kit_root: Path, globs: list[str], max_chars: int = 12000) -> str:
    chunks: list[str] = []
    total = 0
    for pattern in globs:
        for path in sorted(kit_root.glob(pattern)):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            header = f"\n\n--- FILE: {path.relative_to(kit_root)} ---\n"
            piece = header + text
            if total + len(piece) > max_chars:
                remain = max_chars - total
                if remain > 200:
                    chunks.append(piece[:remain] + "\n…(truncated)…\n")
                return "".join(chunks)
            chunks.append(piece)
            total += len(piece)
    return "".join(chunks)
