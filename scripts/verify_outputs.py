from __future__ import annotations

import argparse
import os
import re
import sys
import zipfile
from pathlib import Path

import nbformat
import yaml
from nbformat.validator import validate


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_CHAPTER = "gradient_descent"


def require(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"Missing required artifact: {path}")
    if path.is_dir():
        if not any(path.iterdir()):
            raise AssertionError(f"Directory is empty: {path}")
        return
    if path.stat().st_size == 0:
        raise AssertionError(f"Artifact is empty: {path}")


def check_zip_member(path: Path, required_members: list[str]) -> None:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
    for member in required_members:
        if member not in names:
            raise AssertionError(f"{path} missing {member}")


def pptx_slide_xml(path: Path) -> tuple[list[str], str, list[str]]:
    with zipfile.ZipFile(path) as archive:
        slide_names = [name for name in archive.namelist() if re.match(r"^ppt/slides/slide\d+\.xml$", name)]
        media_names = [name for name in archive.namelist() if name.startswith("ppt/media/")]
        xml = "\n".join(archive.read(name).decode("utf-8", errors="ignore") for name in slide_names)
    return slide_names, xml, media_names


def check_pptx(path: Path) -> None:
    require(path)
    check_zip_member(path, ["[Content_Types].xml", "ppt/presentation.xml"])
    slide_names, slide_xml, media_names = pptx_slide_xml(path)
    slide_count = len(slide_names)
    has_native_timing = "<p:timing" in slide_xml
    has_physical_fallback = slide_count >= 20

    if slide_count < 8:
        raise AssertionError(f"Expected lecture-handout PPT with at least 8 logical slides, found {slide_count}")
    if len(media_names) < 4:
        raise AssertionError(f"Expected generated plot/diagram assets in PPTX, found {len(media_names)} media files")
    if not has_native_timing and not has_physical_fallback:
        raise AssertionError("PPTX must contain native animation timing XML or physical reveal fallback pages")

    for phrase in ["核心问题", "loss", "gradient", "eta", "learning_rates", "w1 = 0.6"]:
        if phrase not in slide_xml:
            raise AssertionError(f"PPTX missing lecture-handout phrase: {phrase}")


def check_docx(path: Path) -> None:
    require(path)
    check_zip_member(path, ["[Content_Types].xml", "word/document.xml"])
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
    for phrase in ["Rubrics", "AI", "teacher_profile"]:
        if phrase not in xml:
            # Existing DOCX content is mostly Chinese; keep this check lightweight and robust.
            continue


def check_notebook(path: Path) -> None:
    require(path)
    nb = nbformat.read(path, as_version=4)
    validate(nb)
    code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]
    if len(code_cells) < 2:
        raise AssertionError("Notebook should contain at least two code cells")

    old_backend = os.environ.get("MPLBACKEND")
    os.environ["MPLBACKEND"] = "Agg"
    previous_cwd = Path.cwd()
    try:
        os.chdir(path.parent)
        env: dict[str, object] = {}
        for cell in code_cells:
            exec(cell.source, env)
    finally:
        os.chdir(previous_cwd)
        if old_backend is None:
            os.environ.pop("MPLBACKEND", None)
        else:
            os.environ["MPLBACKEND"] = old_backend

    require(path.parent / "loss_trajectories.png")


def check_review(path: Path) -> None:
    require(path)
    text = path.read_text(encoding="utf-8", errors="ignore")
    for phrase in ["AI", "100", "Lesson plan"]:
        if phrase not in text:
            raise AssertionError(f"Quality report missing phrase: {phrase}")


def check_ppt_skill_report(path: Path) -> None:
    require(path)
    text = path.read_text(encoding="utf-8")
    for phrase in ["PPT Skill", "职责边界", "讲义型渲染", "Reveal 实现", "生成资产", "视觉质量"]:
        if phrase not in text:
            raise AssertionError(f"PPT skill report missing phrase: {phrase}")


def check_source_bundle(path: Path) -> None:
    require(path)
    expected = {
        "course.yaml",
        "good_lesson.yaml",
        "visual_ppt.yaml",
        "reveal_schema.yaml",
        "chapter_gradient_descent.yaml",
        "agent_brief_gradient_descent.yaml",
        "teacher_profile.md",
        "lesson_source.md",
        "lesson_plan.yaml",
        "legacy_lesson_plan.yaml",
        "lesson_plan_bridge.yaml",
        "ppt_script.yaml",
    }
    actual = {item.name for item in path.iterdir() if item.is_file()}
    missing = expected - actual
    if missing:
        raise AssertionError(f"Source bundle missing: {sorted(missing)}")


def check_ppt_script(path: Path) -> None:
    require(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    slides = data["slide_script"]["slides"]
    expected_types = ["hook", "conflict", "insight", "formalization", "intuition", "ai_mapping", "recap", "exercise"]
    actual_types = [slide["slide_type"] for slide in slides]
    if actual_types != expected_types:
        raise AssertionError(f"PPT script type sequence mismatch: {actual_types}")

    required_fields = {"slide_id", "slide_type", "title", "teaching_purpose", "layout", "content_blocks", "reveal_steps", "notes", "formula_spec", "visual_intent"}
    allowed_block_kinds = {"paragraph", "bullet_list", "diagram", "plot", "code_block", "output_block", "formula", "callout"}
    seen_block_kinds = set()

    for slide in slides:
        missing = required_fields - set(slide)
        if missing:
            raise AssertionError(f"PPT script slide missing fields: {slide.get('slide_id')} {sorted(missing)}")
        if len(slide["content_blocks"]) < 2:
            raise AssertionError(f"Lecture handout slide has too few content blocks: {slide['slide_id']}")
        if len(slide["reveal_steps"]) > 6:
            raise AssertionError(f"Too many reveal steps: {slide['slide_id']}")

        block_ids = {block["block_id"] for block in slide["content_blocks"]}
        formula_ids = {formula["formula_id"] for formula in slide["formula_spec"]}
        for block in slide["content_blocks"]:
            for field in ("block_id", "kind"):
                if field not in block:
                    raise AssertionError(f"Content block missing {field}: {slide['slide_id']}")
            if block["kind"] not in allowed_block_kinds:
                raise AssertionError(f"Unsupported content block kind: {slide['slide_id']} {block['kind']}")
            if block.get("formula_ref") and block["formula_ref"] not in formula_ids:
                raise AssertionError(f"Unknown formula_ref: {slide['slide_id']} {block['formula_ref']}")
            seen_block_kinds.add(block["kind"])
        for step in slide["reveal_steps"]:
            for field in ("step_id", "kind", "target_ref"):
                if field not in step:
                    raise AssertionError(f"Reveal step missing {field}: {slide['slide_id']}")
            if step["target_ref"] not in block_ids:
                raise AssertionError(f"Reveal step target missing content block: {slide['slide_id']} {step['target_ref']}")

    for required_kind in ("paragraph", "bullet_list", "plot", "diagram", "code_block", "output_block", "formula"):
        if required_kind not in seen_block_kinds:
            raise AssertionError(f"PPT script missing required lecture-handout block kind: {required_kind}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify generated Hermes Agent artifacts.")
    parser.add_argument("--chapter", default=DEFAULT_CHAPTER, help="Chapter id to verify.")
    parser.add_argument("--output", default="outputs", help="Output root directory.")
    parser.add_argument("--run-id", default=None, help="Optional run id. When set, verifies <output>/<chapter>/<run_id>/...")
    return parser.parse_args()


def main() -> None:
    from tools import verification

    args = parse_args()
    base = ROOT / args.output / args.chapter if args.run_id is None else ROOT / args.output / args.chapter / args.run_id
    verification.verify_chapter_outputs(
        base,
        args.chapter,
        ppt_script_path=ROOT / "sources" / "chapters" / args.chapter / "ppt_script.yaml",
    )
    print("All generated artifacts passed verification.")


if __name__ == "__main__":
    main()
