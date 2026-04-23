from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt as PptPt


SLIDE_W = 13.333
SLIDE_H = 7.5


def add_text(
    slide,
    text: str,
    left: float,
    top: float,
    width: float,
    height: float,
    size: int,
    *,
    bold: bool = False,
    color: RGBColor | None = None,
    align=PP_ALIGN.LEFT,
    font_name="Microsoft YaHei",
):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    frame = box.text_frame
    frame.word_wrap = True
    frame.clear()
    paragraph = frame.paragraphs[0]
    paragraph.text = text
    paragraph.alignment = align
    for run in paragraph.runs:
        run.font.name = font_name
        run.font.size = PptPt(size)
        run.font.bold = bold
        if color is not None:
            run.font.color.rgb = color
    return box


def add_rect(slide, left: float, top: float, width: float, height: float, fill: RGBColor, line: RGBColor | None = None):
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line or fill
    return shape


def formula_lookup(slide_data: dict) -> dict[str, str]:
    return {item["formula_id"]: item["latex"] for item in slide_data["formula_spec"]}


def step_display_text(slide_data: dict, step: dict) -> tuple[str, bool]:
    if step["kind"] == "formula":
        latex = formula_lookup(slide_data)[step["formula_ref"]]
        return f"\\[{latex}\\]", True
    return step["text"], False


def add_reveal_items(slide, slide_data: dict, steps: list[dict], left: float, top: float, width: float, *, center: bool = False) -> None:
    for index, step in enumerate(steps):
        text, is_formula = step_display_text(slide_data, step)
        y = top + index * (0.72 if is_formula else 0.56)
        font_size = 22 if is_formula else 20
        font = "Cambria Math" if is_formula else "Microsoft YaHei"
        align = PP_ALIGN.CENTER if center or is_formula else PP_ALIGN.LEFT
        color = RGBColor(17, 24, 39) if index == len(steps) - 1 else RGBColor(107, 114, 128)
        add_text(slide, text, left, y, width, 0.45, font_size, color=color, align=align, font_name=font)


def add_slide_chrome(slide, slide_data: dict, reveal_index: int, reveal_count: int, palette: dict[str, RGBColor]) -> None:
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = palette["bg"]
    add_text(slide, slide_data["title"], 0.72, 0.56, 10.6, 0.52, 28, bold=True, color=palette["ink"])
    add_text(
        slide,
        f"{slide_data['slide_id']} · {slide_data['slide_type']} · {reveal_index + 1}/{reveal_count}",
        10.55,
        6.84,
        2.05,
        0.24,
        9,
        color=palette["muted"],
        align=PP_ALIGN.RIGHT,
    )
    add_rect(slide, 0.72, 6.55, 11.9, 0.02, palette["rule"])


def render_center_question(slide, slide_data: dict, visible_steps: list[dict], palette: dict[str, RGBColor]) -> None:
    add_text(slide, slide_data["content"], 1.2, 2.55, 10.9, 0.85, 44, bold=True, color=palette["ink"], align=PP_ALIGN.CENTER)
    add_reveal_items(slide, slide_data, visible_steps, 3.2, 4.05, 6.9, center=True)


def render_two_column(slide, slide_data: dict, visible_steps: list[dict], palette: dict[str, RGBColor]) -> None:
    add_text(slide, slide_data["content"], 0.9, 2.05, 4.6, 1.25, 34, bold=True, color=palette["ink"])
    add_rect(slide, 6.35, 1.62, 0.03, 3.95, palette["rule"])
    add_reveal_items(slide, slide_data, visible_steps, 7.0, 2.08, 4.8)


def render_formula_stage(slide, slide_data: dict, visible_steps: list[dict], palette: dict[str, RGBColor]) -> None:
    add_text(slide, slide_data["content"], 1.2, 1.36, 10.9, 0.45, 20, color=palette["muted"], align=PP_ALIGN.CENTER)
    add_reveal_items(slide, slide_data, visible_steps, 1.3, 2.35, 10.7, center=True)


def render_center_highlight(slide, slide_data: dict, visible_steps: list[dict], palette: dict[str, RGBColor]) -> None:
    add_rect(slide, 1.25, 2.02, 10.85, 2.5, palette["soft"])
    add_text(slide, slide_data["content"], 1.6, 2.42, 10.1, 0.72, 38, bold=True, color=palette["accent"], align=PP_ALIGN.CENTER)
    add_reveal_items(slide, slide_data, visible_steps, 3.05, 3.55, 7.3, center=True)


def add_notes(slide, notes: str) -> None:
    notes_frame = slide.notes_slide.notes_text_frame
    notes_frame.text = notes


def render_pptx(slide_script: dict, visual_config: dict, output_path: Path) -> None:
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)

    palette = {
        "bg": RGBColor(250, 250, 249),
        "ink": RGBColor(17, 24, 39),
        "muted": RGBColor(107, 114, 128),
        "accent": RGBColor(37, 99, 235),
        "soft": RGBColor(239, 246, 255),
        "rule": RGBColor(229, 231, 235),
    }
    renderers = {
        "center_question": render_center_question,
        "two_column_tension": render_two_column,
        "center_highlight": render_center_highlight,
        "two_column_analogy": render_two_column,
        "formula_stage": render_formula_stage,
        "process_mapping": render_two_column,
    }
    type_rendering = visual_config["visual_ppt"]["slide_type_rendering"]

    for slide_data in slide_script["slide_script"]["slides"]:
        renderer_name = type_rendering[slide_data["slide_type"]]
        renderer = renderers[renderer_name]
        reveal_steps = slide_data["reveal_steps"]
        for reveal_index in range(len(reveal_steps)):
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            add_slide_chrome(slide, slide_data, reveal_index, len(reveal_steps), palette)
            renderer(slide, slide_data, reveal_steps[: reveal_index + 1], palette)
            add_notes(slide, slide_data["notes"])

    prs.save(output_path)


def write_ppt_skill_report(slide_script: dict, visual_config: dict, output_path: Path) -> None:
    root = slide_script["slide_script"]
    visual = visual_config["visual_ppt"]
    verdict = root["visual_verdict"]
    lines = [
        f"# {root['title']} PPT Skill 报告",
        "",
        "## 职责边界",
        "",
        f"- {visual['purpose']}",
    ]
    lines.extend([f"- {item}" for item in visual["boundary"]])
    lines.extend([
        "",
        "## Reveal Schema",
        "",
        f"- 逻辑页：{len(root['slides'])}",
        f"- 物理 reveal 页：{sum(len(slide['reveal_steps']) for slide in root['slides'])}",
        f"- 实现方式：{visual['animation_rule']}",
        "",
        "## 视觉质量",
        "",
        f"- 结论：{verdict['verdict']}",
        f"- 总分：{verdict['total_score']} / 100",
        f"- 通过阈值：{verdict['pass_threshold']}",
        "",
        "## 风险",
        "",
    ])
    lines.extend([f"- {item}" for item in verdict["risks"]])
    lines.extend([
        "",
        "## 修复动作",
        "",
    ])
    lines.extend([f"- {item}" for item in verdict["repair_actions"]])
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
