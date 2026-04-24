from __future__ import annotations

from pathlib import Path

from scripts import ppt_skill as legacy


def render_pptx(slide_script: dict, visual_config: dict, output_path: Path) -> None:
    legacy.render_pptx(slide_script, visual_config, output_path)


def write_ppt_skill_report(slide_script: dict, visual_config: dict, output_path: Path) -> None:
    legacy.write_ppt_skill_report(slide_script, visual_config, output_path)
