from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from typing import Any


STAGE_SPECS = {
    "讲前判断": {"alias": "precheck", "node_type": "diagnostic"},
    "讲前判断与驱动问题": {"alias": "precheck", "node_type": "diagnostic"},
    "驱动问题": {"alias": "hook", "node_type": "hook"},
    "玩具模型": {"alias": "toy-model", "node_type": "model"},
    "核心推导": {"alias": "derivation", "node_type": "derivation"},
    "AI 映射": {"alias": "ai-mapping", "node_type": "ai_mapping"},
    "课堂实验": {"alias": "experiment", "node_type": "experiment"},
    "误区处理": {"alias": "misconception", "node_type": "misconception"},
    "课堂检查": {"alias": "check", "node_type": "check"},
    "作业评价": {"alias": "homework", "node_type": "assessment"},
    "课后复盘": {"alias": "retrospective", "node_type": "retrospective"},
}


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _slug_for_stage(stage_name: str, index: int) -> tuple[str, str]:
    spec = STAGE_SPECS.get(stage_name)
    if spec:
        return spec["alias"], spec["node_type"]
    alias = f"stage-{index:02d}"
    return alias, "teaching_stage"


def legacy_to_structured(
    legacy: dict[str, Any],
    *,
    chapter_id: str,
    course_id: str,
    teacher_id: str = "unknown",
    run_id: str = "legacy",
) -> tuple[dict[str, Any], dict[str, Any]]:
    structured = {
        "schema_version": "0.1.0",
        "run_id": run_id,
        "chapter_id": chapter_id,
        "course_id": course_id,
        "teacher_id": teacher_id,
        "generated_at": utc_now_iso(),
        "summary": {
            "title": legacy["lesson"]["title"],
            "audience": legacy["lesson"]["audience"],
            "duration_minutes": legacy["lesson"]["duration_minutes"],
            "main_question": legacy["lesson_flow"][0]["purpose"] if legacy.get("lesson_flow") else "",
            "key_takeaway": legacy["lesson"]["key_message"],
        },
        "teaching_spine": list(legacy["lesson"]["fixed_template"]),
        "nodes": [],
        "homework": {"required": bool(legacy.get("homework")), "nodes": []},
    }
    bridge = {
        "summary": {
            "title": "lesson.title",
            "audience": "lesson.audience",
            "duration_minutes": "lesson.duration_minutes",
            "key_takeaway": "lesson.key_message",
        },
        "nodes": {},
        "homework": {},
    }

    classroom_by_stage = {
        item["stage"]: item for item in legacy.get("classroom_timing", []) if isinstance(item, dict) and "stage" in item
    }
    classroom_index_by_stage = {
        item["stage"]: index
        for index, item in enumerate(legacy.get("classroom_timing", []))
        if isinstance(item, dict) and "stage" in item
    }
    misconceptions = legacy.get("misconceptions", [])
    checks = legacy.get("in_class_checks", [])

    for index, item in enumerate(legacy.get("lesson_flow", []), start=1):
        stage_name = item["stage"]
        alias, node_type = _slug_for_stage(stage_name, index)
        node_id = f"{chapter_id}-{alias}"
        timing = classroom_by_stage.get(stage_name, {})
        node = {
            "node_id": node_id,
            "node_type": node_type,
            "order": index,
            "title": stage_name,
            "main_question": item["purpose"],
            "key_takeaway": item["core_content"],
            "bridge": {
                "enabled": node_type in {"diagnostic", "derivation", "ai_mapping"},
                "difficulty": "medium" if node_type in {"derivation", "experiment"} else "low",
                "time_budget_minutes": int(timing.get("minutes", 0)),
                "skip_condition": "",
            },
            "ai_mapping": {
                "role_in_model": stage_name,
                "explanation": item["core_content"],
            },
            "experiment_observation": {
                "required": node_type == "experiment",
                "notes": timing.get("teacher_action", ""),
            },
            "student_evidence": {
                "classroom_action": timing.get("teacher_action", ""),
                "observable_behavior": timing.get("student_evidence", ""),
            },
            "source_refs": [],
        }
        structured["nodes"].append(node)
        bridge["nodes"][node_id] = {
            "title": f"lesson_flow[{index - 1}].stage",
            "main_question": f"lesson_flow[{index - 1}].purpose",
            "key_takeaway": f"lesson_flow[{index - 1}].core_content",
            "ai_mapping.role_in_model": f"lesson_flow[{index - 1}].stage",
            "ai_mapping.explanation": f"lesson_flow[{index - 1}].core_content",
        }
        timing_index = classroom_index_by_stage.get(stage_name)
        if timing_index is not None:
            bridge["nodes"][node_id].update(
                {
                    "student_evidence.classroom_action": f"classroom_timing[{timing_index}].teacher_action",
                    "student_evidence.observable_behavior": f"classroom_timing[{timing_index}].student_evidence",
                    "experiment_observation.notes": f"classroom_timing[{timing_index}].teacher_action",
                    "bridge.time_budget_minutes": f"classroom_timing[{timing_index}].minutes",
                }
            )

    for index, item in enumerate(legacy.get("homework", []), start=1):
        node_id = f"{chapter_id}-homework-{index:02d}"
        node = {
            "node_id": node_id,
            "node_type": "homework",
            "order": index,
            "title": item["type"],
            "questions": [item["question"]],
            "answers": [item["answer"]],
            "scoring_evidence": [item["rubric"]],
        }
        structured["homework"]["nodes"].append(node)
        bridge["homework"][node_id] = {
            "title": f"homework[{index - 1}].type",
            "questions[0]": f"homework[{index - 1}].question",
            "answers[0]": f"homework[{index - 1}].answer",
            "scoring_evidence[0]": f"homework[{index - 1}].rubric",
        }

    for index, item in enumerate(misconceptions, start=1):
        if index <= len(structured["nodes"]):
            structured["nodes"][index - 1].setdefault("misconception_notes", []).append(
                {
                    "misconception": item["misconception"],
                    "correction": item["correction"],
                    "teacher_move": item["teacher_move"],
                }
            )
    for index, item in enumerate(checks, start=1):
        if index <= len(structured["nodes"]):
            structured["nodes"][index - 1].setdefault("checkpoints", []).append(
                {
                    "check": item["check"],
                    "prompt": item["prompt"],
                    "expected": item["expected"],
                }
            )

    return structured, bridge


def _parse_tokens(path: str) -> list[str | int]:
    tokens: list[str | int] = []
    remainder = path
    while remainder:
        if "[" in remainder:
            head, rest = remainder.split("[", 1)
            if head:
                for part in head.split("."):
                    if part:
                        tokens.append(part)
            index_text, remainder = rest.split("]", 1)
            tokens.append(int(index_text))
            remainder = remainder[1:] if remainder.startswith(".") else remainder
            continue
        for part in remainder.split("."):
            if part:
                tokens.append(part)
        break
    return tokens


def _set_legacy_path(document: Any, path: str, value: Any) -> None:
    tokens = _parse_tokens(path)
    cursor = document
    for token in tokens[:-1]:
        cursor = cursor[token]
    cursor[tokens[-1]] = value


def _read_node_field(node: dict[str, Any], field_path: str) -> Any:
    tokens = _parse_tokens(field_path)
    cursor: Any = node
    for token in tokens:
        cursor = cursor[token]
    return cursor


def structured_to_legacy(
    structured: dict[str, Any],
    *,
    legacy_template: dict[str, Any],
    bridge: dict[str, Any],
) -> dict[str, Any]:
    updated = deepcopy(legacy_template)

    for field_path, legacy_path in bridge.get("summary", {}).items():
        value = _read_node_field(structured["summary"], field_path)
        _set_legacy_path(updated, legacy_path, value)

    node_lookup = {node["node_id"]: node for node in structured.get("nodes", [])}
    for node_id, mappings in bridge.get("nodes", {}).items():
        node = node_lookup.get(node_id)
        if not node:
            continue
        for field_path, legacy_path in mappings.items():
            value = _read_node_field(node, field_path)
            _set_legacy_path(updated, legacy_path, value)

    homework_lookup = {node["node_id"]: node for node in structured.get("homework", {}).get("nodes", [])}
    for node_id, mappings in bridge.get("homework", {}).items():
        node = homework_lookup.get(node_id)
        if not node:
            continue
        for field_path, legacy_path in mappings.items():
            value = _read_node_field(node, field_path)
            _set_legacy_path(updated, legacy_path, value)

    updated["lesson"]["key_message"] = structured["summary"]["key_takeaway"]
    return updated
