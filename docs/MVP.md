# MVP 实现说明

## 目标

第一版 MVP 验证 PRD 中的单章备课闭环：教师输入“研究生课程，主题：梯度下降与优化，目标是让学生理解模型为什么能通过误差学习”，系统生成可编辑课件、教学包、实验 notebook 和质量门禁报告。

## 实现边界

- 不做 Web 工作台。
- 不接外部 LLM/API。
- 不自动抓取未审查的外部资料。
- 采用文件型资产库，便于教师审校、复用和版本管理。

## Agent / Subagent / Skill 链路

稳定架构是：

`Professor Architect Agent -> Subagent 结构化脚本 -> Skill 稳定执行文件产物`

1. `Professor Architect Agent` 负责课程理解、教学编排、任务分发与质量闭环。
   - 当前实现：`lesson_planner.py` 代表主 Agent 的 lesson plan 编排与 DOCX 教学包生成。
   - 输入：`configs/course.yaml`、`configs/chapters/gradient_descent.yaml`、`configs/quality/good_lesson.yaml`、`sources/chapters/gradient_descent/content.yaml`。
   - 输出：DOCX 教学包、教学质量门禁报告。
   - 禁止：最终 PPT 版式、字体、颜色、坐标、公式渲染和最终文件工艺。
2. `PPT Script Subagent` 只负责把 lesson plan 转成 slide script。
   - 当前实现：`ppt_subagent.py` 校验 slide script 与 reveal schema。
   - 输入：`sources/chapters/gradient_descent/ppt_script.yaml`、`schemas/reveal_schema.yaml`。
   - 中间层：slide type、reveal steps、notes、formula spec、visual intent。
   - 禁止：输出最终 PPTX、发明教学内容、指定最终版式。
3. `Notebook Lab Subagent` 只负责把 lesson plan 转成 notebook 实验脚本。
   - 当前 MVP 折中：notebook 逻辑暂内嵌在 `lesson_planner.py` 中。
   - 目标中间层：实验目标、代码单元、观察问题、预期现象。
   - 禁止：直接输出最终 IPYNB、改变 lesson plan 的教学主线。
4. Skill 只负责稳定执行结构化脚本。
   - `ppt_skill.py` 对应 `ppt_designer`，输入 slide script 与 `configs/quality/visual_ppt.yaml`，输出 PPTX 和 PPT skill 报告。
   - `verify_outputs.py` 对应 `verification`，检查产物完整性、source bundle 和关键质量门禁。
   - 后续 `formula_renderer` 从 PPT 公式处理里拆出，`notebook_builder` 从 notebook 文件生成里拆出。
   - 禁止：自行发明教学内容、改变教学顺序。

## 接口与返工规则

- `lesson_plan.yaml` 是主 Agent 到所有 subagent 的唯一教学内容源。
- `ppt_script.yaml` 只能描述 slide type、reveal steps、notes、formula spec、visual intent，不包含坐标、字体、颜色或最终版式。
- notebook 中间脚本应只描述实验目标、代码单元、观察问题、预期现象，不直接决定最终文件包装。
- `Quality Review Subagent` 只给是否可上课、问题清单、修改建议和应返工责任方，不直接改内容。
- 教学主线问题由 `Professor Architect Agent` 修 lesson plan。
- PPT 结构问题由 `PPT Script Subagent` 修 slide script。
- 实验问题由 `Notebook Lab Subagent` 修 notebook script。
- 文件工艺问题由对应 skill 重新执行。

## 验收方式

运行：

```powershell
.\.venv\Scripts\python scripts\generate_chapter.py --chapter gradient_descent
.\.venv\Scripts\python scripts\verify_outputs.py --chapter gradient_descent
```

验证器检查：

- PPTX 和 DOCX 是有效 OOXML zip 包。
- PPTX 至少包含 20 个 reveal 展开页。
- DOCX 包含章节、作业和评分关键词。
- IPYNB 符合 notebook v4 格式。
- Notebook 代码可执行，并生成 `loss_trajectories.png`。
- 质量报告包含“教学可讲、数学可信、AI 连接有效”和四个章节关键问题。
- DOCX 与质量报告包含“我会不会拿去上课”“什么叫好课”“固定教学模板”“风险与修复动作”。
- PPTX 由 reveal steps 展开为逐步讲解页，不一次性展示全部内容。
- PPT skill 报告包含职责边界、Reveal Schema、物理 reveal 页和视觉质量。
- source bundle 同时保留课程配置、好课标准、视觉标准、reveal schema、章节配置、agent brief、教师画像、lesson plan 和 slide script。
- PRD、README、MVP 与 agent brief 中的 agent/subagent/skill 命名一致。
- 不存在主 Agent 直接生成最终 PPTX、skill 自行补充教学内容、Quality Review 直接改内容的职责描述。
