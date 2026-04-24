from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import ppt_subagent
from tools import lesson_plan_builder, lesson_plan_contracts, notebook_builder, ppt_designer, release_packager, run_state

DEFAULT_CHAPTER = "gradient_descent"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def infer_course_id(course: dict) -> str:
    configured = course.get("course", {}).get("id")
    if configured:
        return str(configured)
    return "ai_math_foundations"


def ensure_output_dirs(output_root: Path, chapter_id: str, run_id: str | None = None) -> dict[str, Path]:
    base = output_root / chapter_id if run_id is None else output_root / chapter_id / run_id
    dirs = {
        "base": base,
        "pptx": base / "pptx",
        "docx": base / "docx",
        "ipynb": base / "ipynb",
        "review": base / "review",
        "review_summary": base / "review" / "summary",
        "release": base / "release" / "teaching",
        "runtime": base / "runtime",
        "source_bundle": base / "source_bundle",
    }
    for directory in dirs.values():
        directory.mkdir(parents=True, exist_ok=True)
    return dirs


def copy_static_source_bundle(chapter_id: str, dirs: dict[str, Path]) -> None:
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
        (ROOT / "sources" / "chapters" / chapter_id / "ppt_script.yaml", "ppt_script.yaml"),
    ]
    for source, target_name in targets:
        shutil.copy2(source, dirs["source_bundle"] / target_name)


def write_source_bundle(
    chapter_id: str,
    dirs: dict[str, Path],
    *,
    lesson_plan: dict,
    structured_lesson_plan: dict,
    lesson_plan_bridge: dict,
) -> None:
    copy_static_source_bundle(chapter_id, dirs)
    bundle = dirs["source_bundle"]
    (bundle / "legacy_lesson_plan.yaml").write_text(
        yaml.safe_dump(lesson_plan, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    (bundle / "lesson_plan.yaml").write_text(
        yaml.safe_dump(structured_lesson_plan, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    (bundle / "lesson_plan_bridge.yaml").write_text(
        yaml.safe_dump(lesson_plan_bridge, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def generate(chapter_id: str, output_root: Path, *, run_id: str | None = None) -> dict[str, Path]:
    course = load_yaml(ROOT / "configs" / "course.yaml")
    good_lesson = load_yaml(ROOT / "configs" / "quality" / "good_lesson.yaml")
    visual_config = load_yaml(ROOT / "configs" / "quality" / "visual_ppt.yaml")
    reveal_schema = load_yaml(ROOT / "schemas" / "reveal_schema.yaml")
    chapter = load_yaml(ROOT / "configs" / "chapters" / f"{chapter_id}.yaml")
    lesson_plan = load_yaml(ROOT / "sources" / "chapters" / chapter_id / "content.yaml")
    slide_script = load_yaml(ROOT / "sources" / "chapters" / chapter_id / "ppt_script.yaml")
    teacher_profile = (ROOT / "profiles" / "teacher_profile.md").read_text(encoding="utf-8")

    lesson_plan_builder.validate_lesson_plan(lesson_plan, good_lesson)
    ppt_subagent.validate_slide_script(slide_script, reveal_schema)

    effective_run_id = run_id or "legacy"
    dirs = ensure_output_dirs(output_root, chapter_id, run_id=run_id)
    requested_outputs = ["pptx", "docx", "ipynb"]
    outputs = {
        "pptx": dirs["pptx"] / f"{chapter_id}.pptx",
        "ppt_report": dirs["pptx"] / "ppt_skill_report.md",
        "docx": dirs["docx"] / "teaching_pack.docx",
        "ipynb": dirs["ipynb"] / f"{chapter_id}_lab.ipynb",
        "review": dirs["review"] / "quality_check.md",
        "teacher_summary": dirs["review_summary"] / "teacher_summary.md",
        "release_manifest": dirs["base"] / "release_manifest.yaml",
        "run_state": dirs["runtime"] / "run_state.yaml",
    }
    structured_lesson_plan, lesson_plan_bridge = lesson_plan_contracts.legacy_to_structured(
        lesson_plan,
        chapter_id=chapter_id,
        course_id=infer_course_id(course),
        teacher_id="unknown",
        run_id=effective_run_id,
    )

    in_progress_state = run_state.build_run_state(
        run_id=effective_run_id,
        chapter_id=chapter_id,
        status="generating",
        requested_outputs=requested_outputs,
    )
    run_state.write_run_state(in_progress_state, outputs["run_state"])

    lesson_plan_builder.build_docx(course, chapter, lesson_plan, good_lesson, teacher_profile, outputs["docx"])
    notebook_builder.build_notebook(lesson_plan, outputs["ipynb"])
    lesson_plan_builder.write_quality_report(course, chapter, lesson_plan, good_lesson, outputs["review"])
    ppt_designer.render_pptx(slide_script, visual_config, outputs["pptx"])
    ppt_designer.write_ppt_skill_report(slide_script, visual_config, outputs["ppt_report"])
    teacher_summary_lines = release_packager.build_teacher_summary(
        chapter_title=lesson_plan["lesson"]["title"],
        run_id=effective_run_id,
        quality_verdict=lesson_plan["teacher_quality_review"]["verdict"],
        total_score=lesson_plan["teacher_quality_review"]["total_score"],
        output_paths=outputs,
    )
    release_packager.write_teacher_summary(teacher_summary_lines, outputs["teacher_summary"])
    gate_passed = lesson_plan["teacher_quality_review"]["total_score"] >= lesson_plan["teacher_quality_review"]["pass_threshold"]
    manifest = release_packager.build_release_manifest(
        run_id=effective_run_id,
        chapter_id=chapter_id,
        output_paths=outputs,
        gate_passed=gate_passed,
    )
    release_packager.write_release_manifest(manifest, outputs["release_manifest"])
    final_state = run_state.build_run_state(
        run_id=effective_run_id,
        chapter_id=chapter_id,
        status="released" if gate_passed else "blocked",
        requested_outputs=requested_outputs,
        gate_passed=gate_passed,
        started_at=in_progress_state["started_at"],
    )
    final_state["artifacts"] = {
        "teacher_summary": str(outputs["teacher_summary"]),
        "release_manifest": str(outputs["release_manifest"]),
    }
    run_state.write_run_state(final_state, outputs["run_state"])
    write_source_bundle(
        chapter_id,
        dirs,
        lesson_plan=lesson_plan,
        structured_lesson_plan=structured_lesson_plan,
        lesson_plan_bridge=lesson_plan_bridge,
    )
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Hermes Agent chapter artifacts.")
    parser.add_argument("--chapter", default=DEFAULT_CHAPTER, help="Chapter id to generate.")
    parser.add_argument("--output", default="outputs", help="Output root directory.")
    parser.add_argument("--run-id", default=None, help="Optional run id. When set, artifacts are written to <output>/<chapter>/<run_id>/...")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_id = args.run_id or None
    outputs = generate(args.chapter, ROOT / args.output, run_id=run_id)
    print("Generated chapter artifacts:")
    for kind, path in outputs.items():
        print(f"- {kind}: {path}")


if __name__ == "__main__":
    main()
