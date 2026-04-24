from __future__ import annotations

from pathlib import Path

from scripts import lesson_planner as legacy


def validate_lesson_plan(content: dict, good_lesson: dict) -> None:
    legacy.validate_lesson_plan(content, good_lesson)


def build_docx(course: dict, chapter: dict, content: dict, good_lesson: dict, teacher_profile: str, output_path: Path) -> None:
    legacy.build_docx(course, chapter, content, good_lesson, teacher_profile, output_path)


def write_quality_report(course: dict, chapter: dict, content: dict, good_lesson: dict, output_path: Path) -> None:
    legacy.write_quality_report(course, chapter, content, good_lesson, output_path)
