from __future__ import annotations

from pathlib import Path

import yaml

from tools import run_state as run_state_tool


def read_yaml_status(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data if isinstance(data, dict) else {"value": data}


def summarize_run(run_root: Path) -> dict[str, str | bool]:
    review_summary = run_root / "review" / "summary" / "teacher_summary.md"
    manifest = run_root / "release_manifest.yaml"
    run_state_path = run_root / "runtime" / "run_state.yaml"
    run_state = run_state_tool.read_run_state(run_state_path) if run_state_path.exists() else {}
    return {
        "run_root": str(run_root),
        "has_teacher_summary": review_summary.exists(),
        "has_manifest": manifest.exists(),
        "has_run_state": run_state_path.exists(),
        "status": run_state.get("status", "unknown"),
        "updated_at": run_state.get("updated_at", ""),
    }
