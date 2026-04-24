# Intellectual Tutor Hermes Course App Implementation Plan

## Objective

基于新的 PRD，把 `D:\Codex_Project\intellectual_tutor` 从“本地单章生成脚本仓库”升级为：

- 一个运行在官方 `Hermes Agent` 之上的课程备课 app。
- 使用官方 `WeCom` adapter 作为教师入口。
- 支持“生成上课包 + 查询状态 + 提修改 + 二次确认后重生成”的 v1 教师闭环。

本计划明确废弃“自建 Hermes runtime / 自建消息网关 / 自建记忆系统”路线。

## Fixed Architecture

### Official Hermes Core

外部依赖，不在本仓库中重造：

- Memory / summary / cleanup
- Session / gateway / adapter framework
- Agent runtime
- Tool calling and subagent orchestration

### Intellectual Tutor Course App

本仓库负责：

- 课程主 agent 与 subagent 配置
- 课程 workflow contracts
- 章节生成与审查工具
- WeCom 对接说明
- 本机 WSL2 部署说明

### WeCom Entry

第一版固定使用官方 Hermes `WeCom` adapter，不自建新的聊天入口框架。

## Milestones

### M1. Hermes Integration Skeleton

目标：先把本仓库变成“可被 Hermes 挂载的课程 app”，而不是继续直接跑裸脚本。

交付物：

- `docs/deployment/hermes-wsl2-setup.md`
- `docs/deployment/wecom-setup.md`
- `docs/architecture/course-app-overview.md`
- `configs/hermes/` 下的 app 配置草案
- `skills/` 或 Hermes 要求的课程 skill 目录骨架
- `agents/` 或 Hermes 要求的主 agent / subagent prompt 骨架

任务：

1. 研究并固定官方 Hermes 本地接入方式
2. 定义本仓库的 Hermes 挂载目录结构
3. 把当前课程能力映射为：
   - SOUL / persona
   - main agent
   - subagents
   - skills
   - tools
4. 明确 Windows 路径到 WSL2 路径的访问约束

验收：

- 可以清楚回答“本仓库中的哪些文件会被 Hermes 直接加载”
- 可写出一套最小 Hermes 接入目录，不再依赖口头约定

### M2. Workflow Contract Refactor

目标：把当前脚本链重构成 Hermes 友好的结构化 contracts。

交付物：

- `schemas/course/lesson_plan.yaml`
- `schemas/course/ppt_script.yaml`
- `schemas/course/notebook_script.yaml`
- `schemas/course/quality_review.yaml`
- `schemas/course/release_manifest.yaml`
- `schemas/course/change_request.yaml`
- `schemas/course/change_confirmation.yaml`

任务：

1. 把现有 `content.yaml` 升级为节点化 `lesson_plan` contract
2. 把 PPT contract 与 notebook contract 从脚本实现中抽离
3. 明确 teacher summary / release manifest / review contracts
4. 让所有关键治理链都携带 `run_id`

验收：

- 所有主要 workflow 输入输出都能用结构化文件描述
- 主 agent、subagent、tool 的接口边界可以直接落到文件和 schema 上

### M3. Toolization Of Existing Generators

目标：把当前 Python 脚本从“自由入口脚本”重构成可被 Hermes 调用的 course tools。

交付物：

- `tools/lesson_plan_builder.py`
- `tools/ppt_designer.py`
- `tools/notebook_builder.py`
- `tools/verification.py`
- `tools/release_packager.py`
- `tools/status_reader.py`
- `tools/change_applier.py`

任务：

1. 拆分 `scripts/generate_chapter.py` 的 orchestration 责任
2. 把 `lesson_planner.py` 中 notebook 逻辑独立出来
3. 把 `ppt_skill.py`、`verify_outputs.py` 重命名并改造成 tool 风格接口
4. 统一 tool 的输入输出为：
   - structured input path
   - output root
   - structured result

验收：

- 不再存在一个“大一统脚本”承担所有生成逻辑
- 每个 tool 都有清晰输入、输出、职责和失败语义

### M4. Course Agent And Subagent Setup

目标：把课程 workflow 真正定义成 Hermes 可运行的 agent 体系。

交付物：

- 课程 SOUL / persona
- `Professor Architect Agent` prompt
- `PPT Script Subagent` prompt
- `Notebook Lab Subagent` prompt
- `Quality Review Subagent` prompt
- `Source Curator Subagent` prompt
- 对应 skill 配置

任务：

1. 把新 PRD 中的职责边界转成 prompt / policy / skill 规则
2. 把写入类请求必须二次确认的规则固化进 agent 行为
3. 把“教学内容可改、课程基线不可改”的权限边界写进 course app
4. 把来源治理与 override 规则写进 review 和 source 子链

验收：

- 可以回答每个修改动作由谁决策、谁转译、谁执行
- agent 不直接越权生成最终文件或绕过确认流程

### M5. Run Layout And Release Chain

目标：建立和新 PRD 一致的运行产物目录与发布链。

交付物：

- `outputs/runs/<chapter>/<run_id>/...` 目录规范
- `review/summary/teacher_summary.md`
- `release_manifest.yaml`
- `source_bundle/debug_index.md`

任务：

1. 引入 `run_id` 贯穿所有关键产物
2. 改造输出目录为 run-based layout
3. 增加 `teacher_summary`、`release_manifest`、debug index
4. 区分 release / review / source bundle

验收：

- 多次运行不会互相覆盖
- 老师端回传、调试、回归都能定位到具体 `run_id`

### M6. Teacher Change Loop

目标：实现教师修改摘要与确认闭环。

交付物：

- `change_request.yaml`
- `change_summary.md`
- `change_confirmation.yaml`
- 影响范围判断逻辑

任务：

1. 解析自然语言修改为结构化变更请求
2. 生成自然语言变更摘要
3. 等待明确确认词
4. 按影响范围重跑：
   - lesson plan only
   - ppt regeneration
   - notebook regeneration
   - full review

验收：

- 老师提出修改时系统不会直接改文件
- 未确认前不会触发真正的重生成

### M7. WeCom End-to-End Integration

目标：接通官方 Hermes WeCom adapter 与课程 app。

交付物：

- WeCom 环境变量与配置清单
- 本机回调接入说明
- WeCom smoke test 说明
- 教师交互示例脚本

任务：

1. 配置 Hermes WeCom callback
2. 验证 WeCom 到 Hermes 的消息链路
3. 让课程 app 接住以下意图：
   - generate package
   - query status
   - propose change
   - confirm change
4. 验证附件回传与超限降级

验收：

- 企业微信可以触发一轮真实生成
- 老师能收到摘要、状态和关键附件

### M8. Regression And Local Operations

目标：让这套系统在当前电脑上可稳定重复运行。

交付物：

- 本机启动命令清单
- 日志与诊断说明
- e2e smoke test 文档
- 回归测试说明

任务：

1. 增加本机启动顺序说明
2. 增加 WSL2 / Windows 路径协同说明
3. 增加黄金样例回归脚本或手册
4. 增加常见故障排查

验收：

- 关闭 IDE 后，环境可重新恢复
- 关键链路有明确的 smoke test

## Recommended Build Order

推荐按以下顺序推进：

1. `M1 Hermes Integration Skeleton`
2. `M2 Workflow Contract Refactor`
3. `M3 Toolization Of Existing Generators`
4. `M4 Course Agent And Subagent Setup`
5. `M5 Run Layout And Release Chain`
6. `M6 Teacher Change Loop`
7. `M7 WeCom End-to-End Integration`
8. `M8 Regression And Local Operations`

## Immediate Next Slice

下一步最值得立刻开工的是 `M1`，具体到可执行任务是：

1. 增加 `docs/deployment/hermes-wsl2-setup.md`
2. 增加 `docs/deployment/wecom-setup.md`
3. 增加 `docs/architecture/course-app-overview.md`
4. 新建 Hermes course app 目录骨架：
   - course persona
   - main agent
   - subagents
   - skills
   - tools
5. 写清现有脚本到 future tools 的映射表

只有这一步完成后，后面的 contract 重构和 WeCom 接入才不会继续沿着旧的错误路线走。

## Anti-patterns

- 在本仓库里继续自建 Hermes runtime
- 让企业微信回调直接调用 `generate_chapter.py`
- 把课程 app 做成新的通用智能体底座
- 继续把 notebook 逻辑留在主 agent 中
- 没有 `run_id` 与 release chain 就先做聊天闭环
- 同时维护 Hermes 编排和本仓库外挂编排两套 runtime
