from __future__ import annotations

from pathlib import Path

import yaml


def write_release_manifest(manifest: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False), encoding="utf-8")


def write_teacher_summary(summary_lines: list[str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(summary_lines).rstrip() + "\n", encoding="utf-8")


def build_teacher_summary(*, chapter_title: str, run_id: str, quality_verdict: str, total_score: int, output_paths: dict[str, Path]) -> list[str]:
    return [
        f"# {chapter_title}教师摘要",
        "",
        f"- run_id: {run_id}",
        f"- 结论: {quality_verdict}",
        f"- 总分: {total_score} / 100",
        "",
        "## 主要产物",
        "",
        f"- PPTX: {output_paths['pptx']}",
        f"- DOCX: {output_paths['docx']}",
        f"- IPYNB: {output_paths['ipynb']}",
        f"- Review: {output_paths['review']}",
    ]


def build_release_manifest(*, run_id: str, chapter_id: str, output_paths: dict[str, Path], gate_passed: bool) -> dict:
    return {
        "schema_version": "0.1.0",
        "run_id": run_id,
        "chapter_id": chapter_id,
        "artifact_list": [
            {"artifact_type": "pptx", "path": str(output_paths["pptx"]), "status": "released" if gate_passed else "blocked"},
            {"artifact_type": "docx", "path": str(output_paths["docx"]), "status": "released" if gate_passed else "blocked"},
            {"artifact_type": "ipynb", "path": str(output_paths["ipynb"]), "status": "released" if gate_passed else "blocked"},
            {"artifact_type": "summary", "path": str(output_paths["teacher_summary"]), "status": "released"},
        ],
        "schema_versions": {
            "release_manifest": "0.1.0",
        },
        "gate_result": {
            "passed": gate_passed,
            "blocked_reasons": [],
            "critical_nodes_passed": gate_passed,
        },
    }
