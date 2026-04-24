from __future__ import annotations


def validate_slide_script(slide_script: dict, reveal_schema: dict) -> None:
    root = slide_script.get("slide_script")
    if not isinstance(root, dict):
        raise ValueError("Slide script must have a slide_script mapping root.")

    schema = reveal_schema["reveal_schema"]
    required_slide_fields = schema["required_slide_fields"]
    required_block_fields = schema["required_content_block_fields"]
    required_step_fields = schema["required_reveal_step_fields"]
    allowed_slide_types = set(schema["allowed_slide_types"])
    allowed_layouts = set(schema["allowed_layouts"])
    allowed_content_kinds = set(schema["allowed_content_kinds"])
    allowed_step_kinds = set(schema["allowed_reveal_kinds"])
    slides = root.get("slides", [])
    if not slides:
        raise ValueError("Slide script must contain slides.")

    actual_types = [slide["slide_type"] for slide in slides]
    expected_types = schema["allowed_slide_types"]
    if actual_types != expected_types:
        raise ValueError(f"Slide script must preserve fixed teaching sequence: {actual_types}")

    for slide in slides:
        missing = [field for field in required_slide_fields if field not in slide]
        if missing:
            raise ValueError(f"Slide {slide.get('slide_id', '<unknown>')} missing fields: {', '.join(missing)}")
        if slide["slide_type"] not in allowed_slide_types:
            raise ValueError(f"Unsupported slide type: {slide['slide_type']}")
        if slide["layout"] not in allowed_layouts:
            raise ValueError(f"Unsupported layout in {slide['slide_id']}: {slide['layout']}")
        if len(slide["content_blocks"]) < 2:
            raise ValueError(f"Lecture handout slide needs at least two content blocks: {slide['slide_id']}")
        if len(slide["reveal_steps"]) > 6:
            raise ValueError(f"Slide has too many reveal steps: {slide['slide_id']}")

        formula_ids = {formula["formula_id"] for formula in slide["formula_spec"]}
        block_ids = set()
        for block in slide["content_blocks"]:
            missing_block = [field for field in required_block_fields if field not in block]
            if missing_block:
                raise ValueError(f"Content block missing fields in {slide['slide_id']}: {', '.join(missing_block)}")
            if block["kind"] not in allowed_content_kinds:
                raise ValueError(f"Unsupported content block kind in {slide['slide_id']}: {block['kind']}")
            if block["block_id"] in block_ids:
                raise ValueError(f"Duplicate content block id in {slide['slide_id']}: {block['block_id']}")
            block_ids.add(block["block_id"])
            formula_ref = block.get("formula_ref")
            if formula_ref and formula_ref not in formula_ids:
                raise ValueError(f"Unknown formula_ref in {slide['slide_id']}: {formula_ref}")

        for step in slide["reveal_steps"]:
            missing_step = [field for field in required_step_fields if field not in step]
            if missing_step:
                raise ValueError(f"Reveal step missing fields in {slide['slide_id']}: {', '.join(missing_step)}")
            if step["kind"] not in allowed_step_kinds:
                raise ValueError(f"Unsupported reveal kind in {slide['slide_id']}: {step['kind']}")
            if step["target_ref"] not in block_ids:
                raise ValueError(f"Reveal step target_ref is not a content block in {slide['slide_id']}: {step['target_ref']}")


def summarize_slide_script(slide_script: dict) -> dict:
    root = slide_script["slide_script"]
    return {
        "chapter_id": root["chapter_id"],
        "title": root["title"],
        "logical_slide_count": len(root["slides"]),
        "native_reveal_step_count": sum(len(slide["reveal_steps"]) for slide in root["slides"]),
    }
