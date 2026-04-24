from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import yaml


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_run_state(
    *,
    run_id: str,
    chapter_id: str,
    status: str,
    requested_outputs: list[str],
    gate_passed: bool | None = None,
    started_at: str | None = None,
) -> dict:
    now = utc_now_iso()
    state = {
        "schema_version": "0.1.0",
        "run_id": run_id,
        "chapter_id": chapter_id,
        "teacher_id": "unknown",
        "space_id": "default-course-space",
        "intent_type": "generate_package",
        "status": status,
        "requested_outputs": requested_outputs,
        "started_at": started_at or now,
        "updated_at": now,
    }
    if gate_passed is not None:
        state["gate_result"] = {
            "passed": gate_passed,
            "blocked_reasons": [],
            "critical_nodes_passed": gate_passed,
        }
    return state


def write_run_state(state: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(state, allow_unicode=True, sort_keys=False), encoding="utf-8")


def read_run_state(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data if isinstance(data, dict) else {"value": data}
