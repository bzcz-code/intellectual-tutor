from __future__ import annotations

import argparse
import os
import zipfile
from pathlib import Path

import nbformat
import yaml
from nbformat.validator import validate


ROOT = Path(__file__).resolve().parents[1]
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


def check_pptx(path: Path) -> None:
    require(path)
    check_zip_member(path, ["[Content_Types].xml", "ppt/presentation.xml"])
    with zipfile.ZipFile(path) as archive:
        slide_names = [name for name in archive.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")]
        slide_count = len(slide_names)
        slide_xml = "\n".join(archive.read(name).decode("utf-8", errors="ignore") for name in slide_names)
    if slide_count < 20:
        raise AssertionError(f"Expected reveal-expanded PPT with at least 20 physical slides, found {slide_count}")
    for phrase in ["S01", "hook", "1/3", "参数往哪改", "GPT", "eta=1.05"]:
        if phrase not in slide_xml:
            raise AssertionError(f"PPTX missing visual/reveal phrase: {phrase}")


def check_docx(path: Path) -> None:
    require(path)
    check_zip_member(path, ["[Content_Types].xml", "word/document.xml"])
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    for phrase in ["梯度下降与优化", "讲前判断", "什么叫好课", "固定教学模板", "常见误区", "课堂检查", "作业", "评分"]:
        if phrase not in xml:
            raise AssertionError(f"DOCX missing key phrase: {phrase}")


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

    generated_plot = path.parent / "loss_trajectories.png"
    require(generated_plot)


def check_review(path: Path) -> None:
    require(path)
    text = path.read_text(encoding="utf-8")
    for phrase in ["我会不会拿去上课", "什么叫好课", "总分", "教学可讲", "数学可信", "AI 连接有效", "每章必须回答的四个问题", "风险与修复动作"]:
        if phrase not in text:
            raise AssertionError(f"Quality report missing phrase: {phrase}")


def check_ppt_skill_report(path: Path) -> None:
    require(path)
    text = path.read_text(encoding="utf-8")
    for phrase in ["PPT Skill", "职责边界", "Reveal Schema", "物理 reveal 页", "视觉质量"]:
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
    expected_types = ["hook", "conflict", "insight", "intuition", "formalization", "ai_mapping", "recap", "exercise"]
    actual_types = [slide["slide_type"] for slide in slides]
    if actual_types != expected_types:
        raise AssertionError(f"PPT script type sequence mismatch: {actual_types}")
    required_fields = {"slide_id", "slide_type", "title", "teaching_purpose", "content", "reveal_steps", "notes", "formula_spec", "visual_intent"}
    for slide in slides:
        missing = required_fields - set(slide)
        if missing:
            raise AssertionError(f"PPT script slide missing fields: {slide.get('slide_id')} {sorted(missing)}")
        if len(slide["reveal_steps"]) > 4:
            raise AssertionError(f"Too many reveal steps: {slide['slide_id']}")
        if len(slide["content"]) > 40:
            raise AssertionError(f"Slide content too long: {slide['slide_id']}")
        for step in slide["reveal_steps"]:
            for field in ("step_id", "kind", "text"):
                if field not in step:
                    raise AssertionError(f"Reveal step missing {field}: {slide['slide_id']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify generated Hermes Agent artifacts.")
    parser.add_argument("--chapter", default=DEFAULT_CHAPTER, help="Chapter id to verify.")
    parser.add_argument("--output", default="outputs", help="Output root directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base = ROOT / args.output / args.chapter
    check_pptx(base / "pptx" / f"{args.chapter}.pptx")
    check_docx(base / "docx" / "teaching_pack.docx")
    check_notebook(base / "ipynb" / f"{args.chapter}_lab.ipynb")
    check_review(base / "review" / "quality_check.md")
    check_ppt_skill_report(base / "pptx" / "ppt_skill_report.md")
    check_source_bundle(base / "source_bundle")
    check_ppt_script(ROOT / "sources" / "chapters" / args.chapter / "ppt_script.yaml")
    print("All generated artifacts passed verification.")


if __name__ == "__main__":
    main()
