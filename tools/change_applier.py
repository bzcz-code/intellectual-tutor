from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


_PATH_TOKEN_RE = re.compile(r"([^.[]+)(?:\[(\d+)\])?")
_LESSON_FLOW_RE = re.compile(r"^lesson_flow\[(\d+)\]\.(stage|purpose|core_content)$")
_CLASSROOM_TIMING_RE = re.compile(r"^classroom_timing\[(\d+)\]\.(minutes|teacher_action|student_evidence)$")
_HOMEWORK_RE = re.compile(r"^homework\[(\d+)\]\.(type|question|answer|rubric)$")


def _parse_path(path: str) -> list[str | int]:
    if not path:
        return []
    tokens: list[str | int] = []
    for raw_part in path.split("."):
        if not raw_part:
            continue
        match = _PATH_TOKEN_RE.fullmatch(raw_part)
        if not match:
            raise ValueError(f"Unsupported field path segment: {raw_part}")
        name, index = match.groups()
        tokens.append(name)
        if index is not None:
            tokens.append(int(index))
    return tokens


def _ensure_list_size(items: list[Any], index: int) -> None:
    while len(items) <= index:
        items.append({})


def _set_path_value(document: Any, path: str, new_value: Any) -> None:
    tokens = _parse_path(path)
    if not tokens:
        raise ValueError("field path cannot be empty")

    cursor = document
    for index, token in enumerate(tokens[:-1]):
        next_token = tokens[index + 1]
        if isinstance(token, str):
            if not isinstance(cursor, dict):
                raise TypeError(f"Expected mapping while traversing {path!r}")
            if token not in cursor or cursor[token] is None:
                cursor[token] = [] if isinstance(next_token, int) else {}
            cursor = cursor[token]
            continue

        if not isinstance(cursor, list):
            raise TypeError(f"Expected list while traversing {path!r}")
        _ensure_list_size(cursor, token)
        if cursor[token] is None:
            cursor[token] = [] if isinstance(next_token, int) else {}
        cursor = cursor[token]

    last_token = tokens[-1]
    if isinstance(last_token, str):
        if not isinstance(cursor, dict):
            raise TypeError(f"Expected mapping at leaf for {path!r}")
        cursor[last_token] = new_value
        return

    if not isinstance(cursor, list):
        raise TypeError(f"Expected list at leaf for {path!r}")
    _ensure_list_size(cursor, last_token)
    cursor[last_token] = new_value


def _find_node(document: dict[str, Any], node_id: str) -> dict[str, Any]:
    for node in document.get("nodes", []):
        if isinstance(node, dict) and node.get("node_id") == node_id:
            return node

    homework = document.get("homework", {})
    if isinstance(homework, dict):
        iterable = homework.get("nodes", [])
    elif isinstance(homework, list):
        iterable = homework
    else:
        iterable = []

    for node in iterable:
        if isinstance(node, dict) and node.get("node_id") == node_id:
            return node

    raise KeyError(f"Node not found: {node_id}")


def _normalize_legacy_path(target: str, field: str) -> str:
    if target in {"", "lesson_plan"}:
        return field
    if target.startswith("lesson_plan.") and not target.startswith("lesson_plan.nodes.") and not target.startswith("lesson_plan.homework.nodes."):
        prefix = target.removeprefix("lesson_plan.")
        return f"{prefix}.{field}" if field else prefix
    return field


def _translate_legacy_field_for_structured(document: dict[str, Any], field_path: str) -> str:
    if "summary" not in document:
        return field_path

    direct = {
        "lesson.title": "summary.title",
        "lesson.audience": "summary.audience",
        "lesson.duration_minutes": "summary.duration_minutes",
        "lesson.key_message": "summary.key_takeaway",
    }
    if field_path in direct:
        return direct[field_path]

    match = _LESSON_FLOW_RE.match(field_path)
    if match:
        idx, leaf = int(match.group(1)), match.group(2)
        leaf_map = {
            "stage": "title",
            "purpose": "main_question",
            "core_content": "key_takeaway",
        }
        return f"nodes[{idx}].{leaf_map[leaf]}"

    match = _CLASSROOM_TIMING_RE.match(field_path)
    if match:
        idx, leaf = int(match.group(1)), match.group(2)
        leaf_map = {
            "minutes": "bridge.time_budget_minutes",
            "teacher_action": "student_evidence.classroom_action",
            "student_evidence": "student_evidence.observable_behavior",
        }
        return f"nodes[{idx}].{leaf_map[leaf]}"

    match = _HOMEWORK_RE.match(field_path)
    if match:
        idx, leaf = int(match.group(1)), match.group(2)
        leaf_map = {
            "type": "homework.nodes[{idx}].title",
            "question": "homework.nodes[{idx}].questions[0]",
            "answer": "homework.nodes[{idx}].answers[0]",
            "rubric": "homework.nodes[{idx}].scoring_evidence[0]",
        }
        return leaf_map[leaf].format(idx=idx)

    return field_path


def _apply_change(document: dict[str, Any], change: dict[str, Any]) -> None:
    target = str(change.get("target", "lesson_plan"))
    field = str(change["field"])
    new_value = change["new_value"]

    if target.startswith("lesson_plan.nodes."):
        node_id = target.removeprefix("lesson_plan.nodes.")
        node = _find_node(document, node_id)
        _set_path_value(node, field, new_value)
        return

    if target.startswith("lesson_plan.homework.nodes."):
        node_id = target.removeprefix("lesson_plan.homework.nodes.")
        node = _find_node(document, node_id)
        _set_path_value(node, field, new_value)
        return

    legacy_path = _normalize_legacy_path(target, field)
    legacy_path = _translate_legacy_field_for_structured(document, legacy_path)
    _set_path_value(document, legacy_path, new_value)


def apply_field_changes(source_path: Path, changes: list[dict[str, Any]], output_path: Path | None = None) -> dict[str, Any]:
    with source_path.open("r", encoding="utf-8") as handle:
        document = yaml.safe_load(handle)

    if not isinstance(document, dict):
        raise ValueError(f"Expected mapping YAML: {source_path}")

    updated = deepcopy(document)
    for change in changes:
        _apply_change(updated, change)

    target_path = output_path or source_path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(yaml.safe_dump(updated, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return updated


def build_change_summary(change_request: dict[str, Any]) -> list[str]:
    lines = [
        "# Change Summary",
        "",
        f"- request_id: {change_request['request_id']}",
        f"- run_id: {change_request['run_id']}",
        f"- chapter_id: {change_request['chapter_id']}",
        f"- teacher_id: {change_request['teacher_id']}",
        "",
        "## Original Request",
        "",
        str(change_request["request_text"]),
        "",
        "## Proposed Changes",
        "",
    ]
    for item in change_request.get("proposed_changes", []):
        lines.extend(
            [
                f"- target: {item['target']}",
                f"  - field: {item['field']}",
                f"  - old: {item.get('old_value', '<unknown>')}",
                f"  - new: {item['new_value']}",
                f"  - reason: {item['reason']}",
            ]
        )
    return lines


def write_change_summary(lines: list[str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_override_document(change_request: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "run_id": change_request["run_id"],
        "override_id": change_request["request_id"],
        "teacher_id": change_request["teacher_id"],
        "review_status": "approved",
        "changes": change_request.get("proposed_changes", []),
    }


def append_override_history(change_request: dict[str, Any], history_path: Path) -> None:
    history: list[dict[str, Any]] = []
    if history_path.exists():
        with history_path.open("r", encoding="utf-8") as handle:
            existing = yaml.safe_load(handle)
        if isinstance(existing, list):
            history = existing

    history.append(build_override_document(change_request))
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(yaml.safe_dump(history, allow_unicode=True, sort_keys=False), encoding="utf-8")
