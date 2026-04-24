from __future__ import annotations

from pathlib import Path

from scripts import lesson_planner as legacy


def build_notebook(content: dict, output_path: Path) -> None:
    legacy.build_notebook(content, output_path)
