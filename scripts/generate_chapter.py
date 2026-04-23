from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import yaml

import lesson_planner
import ppt_skill
import ppt_subagent


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHAPTER = "gradient_descent"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def ensure_output_dirs(output_root: Path, chapter_id: str) -> dict[str, Path]:
    base = output_root / chapter_id
    dirs = {
        "base": base,
        "pptx": base / "pptx",
        "docx": base / "docx",
        "ipynb": base / "ipynb",
        "review": base / "review",
        "source_bundle": base / "source_bundle",
    }
    for directory in dirs.values():
        directory.mkdir(parents=True, exist_ok=True)
    return dirs


def copy_source_bundle(chapter_id: str, dirs: dict[str, Path]) -> None:
    for existing in dirs["source_bundle"].iterdir():
        if existing.is_file():
            existing.unlink()

    targets = [
        (ROOT / "configs" / "course.yaml", "course.yaml"),
        (ROOT / "configs" / "quality" / "good_lesson.yaml", "good_lesson.yaml"),
        (ROOT / "configs" / "quality" / "visual_ppt.yaml", "visual_ppt.yaml"),
        (ROOT / "configs" / "chapters" / f"{chapter_id}.yaml", f"chapter_{chapter_id}.yaml"),
        (ROOT / "schemas" / "reveal_schema.yaml", "reveal_schema.yaml"),
        (ROOT / "profiles" / "teacher_profile.md", "teacher_profile.md"),
        (ROOT / "agent_briefs" / f"{chapter_id}.yaml", f"agent_brief_{chapter_id}.yaml"),
        (ROOT / "sources" / "chapters" / chapter_id / "lesson_source.md", "lesson_source.md"),
        (ROOT / "sources" / "chapters" / chapter_id / "content.yaml", "lesson_plan.yaml"),
        (ROOT / "sources" / "chapters" / chapter_id / "ppt_script.yaml", "ppt_script.yaml"),
    ]
    for source, target_name in targets:
        shutil.copy2(source, dirs["source_bundle"] / target_name)


def generate(chapter_id: str, output_root: Path) -> dict[str, Path]:
    course = load_yaml(ROOT / "configs" / "course.yaml")
    good_lesson = load_yaml(ROOT / "configs" / "quality" / "good_lesson.yaml")
    visual_config = load_yaml(ROOT / "configs" / "quality" / "visual_ppt.yaml")
    reveal_schema = load_yaml(ROOT / "schemas" / "reveal_schema.yaml")
    chapter = load_yaml(ROOT / "configs" / "chapters" / f"{chapter_id}.yaml")
    lesson_plan = load_yaml(ROOT / "sources" / "chapters" / chapter_id / "content.yaml")
    slide_script = load_yaml(ROOT / "sources" / "chapters" / chapter_id / "ppt_script.yaml")
    teacher_profile = (ROOT / "profiles" / "teacher_profile.md").read_text(encoding="utf-8")

    lesson_planner.validate_lesson_plan(lesson_plan, good_lesson)
    ppt_subagent.validate_slide_script(slide_script, reveal_schema)

    dirs = ensure_output_dirs(output_root, chapter_id)
    outputs = {
        "pptx": dirs["pptx"] / f"{chapter_id}.pptx",
        "ppt_report": dirs["pptx"] / "ppt_skill_report.md",
        "docx": dirs["docx"] / "teaching_pack.docx",
        "ipynb": dirs["ipynb"] / f"{chapter_id}_lab.ipynb",
        "review": dirs["review"] / "quality_check.md",
    }

    lesson_planner.build_docx(course, chapter, lesson_plan, good_lesson, teacher_profile, outputs["docx"])
    lesson_planner.build_notebook(lesson_plan, outputs["ipynb"])
    lesson_planner.write_quality_report(course, chapter, lesson_plan, good_lesson, outputs["review"])
    ppt_skill.render_pptx(slide_script, visual_config, outputs["pptx"])
    ppt_skill.write_ppt_skill_report(slide_script, visual_config, outputs["ppt_report"])
    copy_source_bundle(chapter_id, dirs)
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Hermes Agent chapter artifacts.")
    parser.add_argument("--chapter", default=DEFAULT_CHAPTER, help="Chapter id to generate.")
    parser.add_argument("--output", default="outputs", help="Output root directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = generate(args.chapter, ROOT / args.output)
    print("Generated chapter artifacts:")
    for kind, path in outputs.items():
        print(f"- {kind}: {path}")


if __name__ == "__main__":
    main()
