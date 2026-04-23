# AI 课程群智能备课 Hermes Agent

面向大学教师的 AI 课程群智能备课 Agent 包，第一阶段聚焦《人工智能数学基础》课程，帮助教师围绕单章主题生成高质量课件、讲稿、实验与作业材料。

## 项目定位

本项目服务讲授 AI 课程群的大学教师，尤其是承担研究生补基础课程的教师。系统以 Hermes Agent 包为第一版产品形态，不做 Web 教师工作台。

核心目标不是替代教师授课，而是成为教师的备课与复盘副驾驶：

- 用 AI 应用问题牵引学生理解数学抽象。
- 帮助教师组织一章课的教学目标、讲解路径、实验和评价。
- 沉淀可复用课程资产，支持后续迁移到机器学习、深度学习、大模型基础等课程。

## MVP 范围

第一版 MVP 以“梯度下降与优化”为黄金样例，验证完整单章备课闭环：

1. AI 应用驱动
2. 数学抽象理解
3. 模型设计解释
4. 实验验证
5. 作业评价

目标输出包括：

- PPTX 课堂课件
- DOCX 教案、讲稿、板书设计、课堂提问、作业与答案
- IPYNB Python 实验 notebook
- Markdown/YAML 中间源稿，用于审校、复用和版本管理

## 长期方向

系统采用“课程模板 + 章节配置 + Professor Architect Agent + Subagent 结构化脚本 + Skill 文件执行”的可迁移结构。梯度下降只是首个验证章节，后续应复用到：

- 矩阵与向量空间
- 概率分布与贝叶斯
- 信息论
- 注意力机制
- 表示学习
- Transformer
- 生成式 AI 基础

详细产品需求见 [docs/PRD.md](docs/PRD.md)。

## 当前 MVP

本仓库已落地第一版文件型 Hermes Agent MVP：以“梯度下降与优化”为黄金样例，通过配置和源稿生成可编辑课堂材料。

### 目录结构

- `configs/course.yaml`：课程级配置。
- `configs/chapters/gradient_descent.yaml`：章节级配置。
- `configs/quality/good_lesson.yaml`：本章“什么叫好课”的教学质量标准。
- `configs/quality/visual_ppt.yaml`：`ppt_designer` skill 的视觉模板与版式规则。
- `schemas/reveal_schema.yaml`：`PPT Script Subagent` 与 `ppt_designer` skill 之间的 reveal 中间层协议。
- `profiles/teacher_profile.md`：默认教师画像。
- `agent_briefs/gradient_descent.yaml`：`Professor Architect Agent`、subagent 与 skill 的职责契约。
- `sources/chapters/gradient_descent/content.yaml`：`Professor Architect Agent` 产出的 lesson plan。
- `sources/chapters/gradient_descent/ppt_script.yaml`：`PPT Script Subagent` 产出的 slide script。
- `scripts/lesson_planner.py`：当前 MVP 中代表 `Professor Architect Agent` 的 lesson plan 编排、DOCX 教学包生成和 notebook 折中实现。
- `scripts/ppt_subagent.py`：校验 `PPT Script Subagent` 的 slide script 与 reveal schema。
- `scripts/ppt_skill.py`：当前 MVP 中的 `ppt_designer` skill，读取 slide script，应用统一 PPT 模板并输出 PPTX。
- `scripts/generate_chapter.py`：只做三层编排，不承担 PPT 视觉设计或教学内容扩写。
- `scripts/verify_outputs.py`：当前 MVP 中的 `verification` skill，验证生成产物。

### 快速运行

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python scripts\generate_chapter.py --chapter gradient_descent
.\.venv\Scripts\python scripts\verify_outputs.py --chapter gradient_descent
```

生成结果位于：

- `outputs/gradient_descent/pptx/gradient_descent.pptx`
- `outputs/gradient_descent/pptx/ppt_skill_report.md`
- `outputs/gradient_descent/docx/teaching_pack.docx`
- `outputs/gradient_descent/ipynb/gradient_descent_lab.ipynb`
- `outputs/gradient_descent/review/quality_check.md`
- `outputs/gradient_descent/source_bundle/`

`outputs/` 是生成物目录，默认不纳入版本管理。

### 质量门禁

当前章节把“好课”定义写死在 `configs/quality/good_lesson.yaml` 中：研究生老师是否愿意在 30 分钟人工微调后拿去上课。教学质量由 `Quality Review Subagent` 的规则约束，MVP 中由 `lesson_planner.py` 写出质量报告；PPT 视觉质量从主生成器中拆出，由 `ppt_skill.py` 按 `visual_ppt.yaml` 和 `reveal_schema.yaml` 单独处理。

当前 MVP 仍保留一个实现折中：notebook 生成逻辑暂在 `lesson_planner.py` 中，后续应拆为 `Notebook Lab Subagent` 产出 notebook 实验脚本，再由 `notebook_builder` skill 稳定生成 IPYNB。这个折中不改变架构边界：subagent 负责结构化脚本，skill 负责最终文件工艺。
