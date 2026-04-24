from __future__ import annotations

from pathlib import Path

from scripts import verify_outputs as legacy


def verify_chapter_outputs(base: Path, chapter_id: str, *, ppt_script_path: Path) -> dict[str, str]:
    legacy.check_pptx(base / "pptx" / f"{chapter_id}.pptx")
    legacy.check_docx(base / "docx" / "teaching_pack.docx")
    legacy.check_notebook(base / "ipynb" / f"{chapter_id}_lab.ipynb")
    legacy.check_review(base / "review" / "quality_check.md")
    legacy.check_ppt_skill_report(base / "pptx" / "ppt_skill_report.md")
    legacy.check_source_bundle(base / "source_bundle")
    legacy.check_ppt_script(ppt_script_path)
    return {
        "status": "passed",
        "chapter_id": chapter_id,
        "base": str(base),
    }
