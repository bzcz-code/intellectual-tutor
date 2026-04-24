from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


SLIDE_NODE_SUFFIX = {
    "hook": "hook",
    "conflict": "precheck",
    "insight": "toy-model",
    "formalization": "derivation",
    "intuition": "experiment",
    "ai_mapping": "ai-mapping",
    "recap": "retrospective",
    "exercise": "check",
}


def _node_lookup(structured_lesson_plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {node["node_id"]: node for node in structured_lesson_plan.get("nodes", [])}


def _find_node_for_slide(chapter_id: str, slide_type: str, nodes: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    suffix = SLIDE_NODE_SUFFIX.get(slide_type)
    if not suffix:
        return None
    return nodes.get(f"{chapter_id}-{suffix}")


def _update_textual_blocks(slide: dict[str, Any], *, summary_text: str) -> None:
    for block in slide.get("content_blocks", []):
        kind = block.get("kind")
        if kind in {"paragraph", "output_block"} and "text" in block:
            block["text"] = summary_text
            return
    for block in slide.get("content_blocks", []):
        kind = block.get("kind")
        if kind == "bullet_list" and block.get("items"):
            block["items"][0] = summary_text
            return


def sync_ppt_script_from_lesson_plan(ppt_script: dict[str, Any], structured_lesson_plan: dict[str, Any]) -> dict[str, Any]:
    updated = deepcopy(ppt_script)
    root = updated["slide_script"]
    summary = structured_lesson_plan["summary"]
    chapter_id = structured_lesson_plan["chapter_id"]
    nodes = _node_lookup(structured_lesson_plan)

    root["title"] = summary["title"]
    root["source_lesson_plan"] = "source_bundle/lesson_plan.yaml"

    for slide in root.get("slides", []):
        node = _find_node_for_slide(chapter_id, slide.get("slide_type", ""), nodes)
        if not node:
            continue
        slide["title"] = node["title"]
        slide["teaching_purpose"] = node["main_question"]
        summary_text = node["key_takeaway"]
        if slide.get("slide_type") == "ai_mapping":
            summary_text = node.get("ai_mapping", {}).get("explanation", summary_text)
        _update_textual_blocks(slide, summary_text=summary_text)
        slide["notes"] = f"{node['main_question']}\n\n{summary_text}"

    return updated


def write_synced_ppt_script(ppt_script: dict[str, Any], output_path: Path) -> None:
    output_path.write_text(yaml.safe_dump(ppt_script, allow_unicode=True, sort_keys=False), encoding="utf-8")
