# Intellectual Tutor: A Hermes Course App

## 1. Product Identity

`Intellectual Tutor` 是一个运行在官方 `Hermes Agent` 之上的课程备课 app，面向讲授 AI 课程群的大学教师，帮助教师围绕单章主题稳定生成高质量上课包，并通过企业微信完成查询、修改、确认和重生成闭环。

本产品不是 Hermes 本体，也不是新的通用智能体框架；它是一个专用于课程备课的 Hermes 垂直应用。

第一阶段聚焦《人工智能数学基础》课程，首个黄金样例是“梯度下降与优化”。

核心目标不是替代教师授课，而是成为教师的备课与复盘副驾驶：

- 用真实 AI 训练问题牵引学生理解数学抽象。
- 帮助教师组织一章课的教学目标、讲解路径、实验和评价。
- 沉淀可复用课程资产，支持后续迁移到机器学习、深度学习、大模型基础等课程。

第一版目标用户：

- 讲授《人工智能数学基础》《机器学习数学基础》《AI 导论数学模块》的大学教师。
- 首次开课或需要重构课程材料的青年教师。
- 负责 AI 课程群建设、需要沉淀课程资产的教学团队。

默认教学定位：

- 面向研究生补基础。
- 中文主讲，保留关键英文术语。
- 应用驱动加理解数学抽象。
- 不是纯数学体系课，也不是工具使用课。

## 2. System Boundary

### 2.1 Official Hermes Core

官方 `Hermes Agent` 是系统底座，运行在本机 `WSL2` 中，负责：

- 持久记忆与跨会话检索。
- 总结沉淀与自我净化。
- 会话与消息网关。
- subagent 调度与 skill/tool 调用框架。
- 长期状态、日志、调试与自动化能力。

这些能力不在本仓库中重造。

### 2.2 Intellectual Tutor Course Layer

本仓库只提供课程层能力：

- 课程主 agent 与 subagent 设计。
- 课程 workflow contracts。
- 教学质量门禁。
- 章节生成、审查、打包与回传逻辑。
- 本机部署说明。
- 企业微信接入配置说明。

### 2.3 WeCom Entry

教师入口直接使用官方 `Hermes Agent` 的 `WeCom (企业微信)` adapter。

企业微信只做教师自然语言入口与附件回传，不承载课程业务逻辑，不自行维护一套 agent runtime。

### 2.4 Non-ownership

本仓库明确不负责：

- 官方 Hermes 的记忆系统实现。
- Hermes 的总结/净化机制实现。
- Hermes gateway 主框架。
- Hermes profile/session/memory 内核。
- 官方平台 adapter 的主实现。

## 3. Deployment Scope And Preconditions

### 3.1 Deployment Scope

第一版部署目标固定为：

- 宿主机：当前这台 Windows 电脑。
- 运行环境：`WSL2`。
- Hermes 实例类型：专用于课程备课的 Hermes 实例。
- 入口渠道：企业微信。

### 3.2 Preconditions

第一版承诺的是“前置条件满足后的全自动部署”，不是零前置全自动。

必须满足的前置条件：

- `WSL2` 已可用。
- 官方 `Hermes Agent` 可在 `WSL2` 中安装运行。
- 企业微信自建应用已创建。
- 所需密钥、`Corp ID`、`Agent ID` 与回调配置已准备完毕。
- 当前仓库位于 Windows 可稳定映射到 WSL2 的工作区路径中。

### 3.3 Repository Role

本仓库角色固定为：

- Hermes 的课程 app / workflow 仓库。
- 本机部署说明仓库。
- WeCom 配置说明仓库。

本仓库不是官方 Hermes 源码镜像，不 vendor 官方 Hermes 本体。

## 4. MVP And v1 Goal

### 4.1 v1 Goal

第一版目标是在官方 Hermes 底座上，完成单章备课闭环的稳定验证：

- 老师通过企业微信发起生成请求。
- Hermes 调用课程 app workflow。
- 生成结构化中间产物和最终上课包。
- 老师可查询状态、提出修改、收到变更摘要并确认。
- 系统按影响范围重生成并回传结果。

### 4.2 Golden Sample

首个黄金样例为“梯度下降与优化”。

老师输入示例：

> 研究生课程，主题：梯度下降与优化，目标是让学生理解模型为什么能通过误差学习。

系统输出：

- PPTX：课堂课件。
- DOCX：教案、讲稿、板书设计、课堂提问、作业、标准答案与评分 rubrics。
- IPYNB：Python 实验 notebook。
- Markdown/YAML 中间源稿：用于审校、复用和版本管理。
- 审查与发布产物：`quality_review.yaml`、`teacher_summary.md`、`release_manifest.yaml`。

### 4.3 Chapter Teaching Chain

单章生成链路固定为：

1. AI 应用驱动：从模型训练、损失函数、参数更新等真实问题切入。
2. 数学抽象理解：解释梯度、方向导数、学习率、收敛等核心概念。
3. 模型设计解释：说明为什么模型可以通过误差反复更新参数。
4. 实验验证：通过 Python notebook 可视化损失下降和参数更新。
5. 作业评价：提供概念题、推导题、实验题、答案和评分标准。

### 4.4 Teacher Loop In Scope

第一版教师闭环固定为：

- 生成上课包。
- 查询状态。
- 提修改。
- 二次确认后重生成。

教师允许修改到：

- 教学内容。
- 章节配置。

教师不得直接修改：

- 系统红线。
- 来源可信规则。
- 课程级质量基线。
- 其他系统治理规则。

## 5. Course App Architecture

### 5.1 Layered Architecture

课程 app 的稳定协作链路为：

`Hermes Core -> Professor Architect Agent -> Subagent 结构化脚本 -> Course Tools / Skills -> 发布与回传`

这里的三层调用含义是：

1. 主 agent 层：理解老师意图、决定 workflow、分发任务、聚合审查结果。
2. subagent / skill 层：把任务转成结构化中间稿与规则化判断。
3. tool 层：读取结构化输入并执行最终文件生成、校验、打包和回传。

### 5.2 Main Agent

课程层主 agent 为 `Professor Architect Agent`。它运行在 Hermes 中，具备大学教师判断力和课程架构编排能力。

职责：

- 理解教师任务。
- 补齐课程上下文。
- 拆解单章备课任务。
- 委派 subagent。
- 产出统一的 `lesson_plan.yaml`。
- 根据质量审查结果发出返工指令。
- 维护教学主线和质量闭环。

禁止：

- 直接承担 PPT 版式。
- 直接承担公式渲染细节。
- 直接承担 notebook 文件工艺。
- 绕过 subagent / tool 直接拼装最终交付件。

### 5.3 Subagents

Subagent 只负责把 `lesson_plan.yaml` 转译成某类产物的结构化脚本，不直接产出最终文件。

- `PPT Script Subagent`
  - 输出：`ppt_script.yaml`
  - 负责：slide 映射、reveal steps、notes、formula spec、visual intent。
- `Notebook Lab Subagent`
  - 输出：`notebook_script.yaml`
  - 负责：实验目标、代码单元、观察问题、预期现象。
- `Quality Review Subagent`
  - 输出：`quality_review.yaml`
  - 负责：审查结论、问题清单、修改建议、返工责任方。
- `Source Curator Subagent`
  - 输出：`source_proposal.yaml`、`source_decision.yaml`、`sources.yaml`
  - 负责：来源筛选、锚点定位、适用范围与可信边界。

### 5.4 Course Skills

Skill 负责稳定固化课程规则和流程知识，不自行发明教学内容。

第一版至少需要：

- 课程备课 workflow skill。
- 教学质量门禁 skill。
- 变更摘要与确认流程 skill。
- 来源治理与补源提示 skill。

### 5.5 Course Tools

Tool 负责执行能力，不负责课程决策。

第一版至少需要：

- `lesson_plan_builder`
- `ppt_designer`
- `formula_renderer`
- `notebook_builder`
- `verification`
- `release_packager`
- `status_reader`
- `change_applier`

## 6. Teacher Interaction Loop

### 6.1 Supported Actions

第一版支持的教师自然语言动作：

- 查询状态。
- 修改教学内容。
- 发起补源。
- 触发复审与重生成。

### 6.2 Write Safety Rule

查询类请求可以直接返回结果。

写入类请求必须遵循：

1. 先输出变更摘要。
2. 再由老师二次确认。
3. 确认后按影响范围重跑。

第一版确认交互形态固定为：

- 文本摘要。
- 明确确认词。

聊天里允许自然语言变更摘要，不要求老师阅读 YAML diff。

### 6.3 Ambiguity Rule

聊天里如章节存在歧义，必须追问，不得静默猜测。

老师连续提出多条修改意见时，系统应支持：

- 先汇总。
- 再一次确认。

老师确认后应立即按影响范围重跑，而不是只写 `override.yaml`。

### 6.4 Scope-aware Regeneration

重跑必须按影响范围进行，而非默认整章重做。

至少区分：

- 只影响 `lesson_plan.yaml`
- 影响 `ppt_script.yaml`
- 影响 `notebook_script.yaml`
- 需要整章复审

## 7. WeCom Entry

### 7.1 Channel Strategy

第一版首选聊天渠道为企业微信（WeCom）。

后续扩展目标为：

- 飞书

第一版不以 Web 教师控制台作为教师主入口。

### 7.2 Space Model

第一版按“先单学科”落地。

当前 v1 入口模型固定为：

- 一个企业微信应用。
- 对应一个学科入口。
- 对应该老师当前这门课的主 agent。

后续扩展路径固定为：

- 单应用多学科入口。

### 7.3 Identity And State

企业微信身份与教师画像在开通时一次绑定。

学科空间聊天状态默认持久保存，至少包括：

- 当前学科。
- 最近章节上下文。
- 待确认修改。
- 最近一次运行结果。
- 最近一次审查状态。

### 7.4 Task Feedback And Delivery

第一版长任务反馈采用：

- 接单确认。
- 关键阶段进度通知。
- 完成通知。

第一版结果回传采用：

- 自然语言摘要。
- 主要文件优先直接发附件。
- 保留整包链接能力。

默认附件回传形态为：

- 摘要。
- 主要文件。
- 可选整包链接。

当附件超限时，当前默认降级策略为：

- 自动拆分多文件。

如必须通过链接回传，链接目标应使用对象存储或文件服务。

## 8. Workflow Contracts

### 8.1 Course And Chapter Config

第一版采用文件型资产库，核心配置以 Markdown/YAML 为主。

`course.yaml` 描述课程级配置：

- 课程名称。
- 目标学生。
- 总学时。
- 课程风格。
- 推导深度。
- 应用案例比例。
- 实验强度。
- 作业难度。
- 语言策略。

`chapter.yaml` 描述章节级配置：

- 章节主题。
- 先修知识。
- 核心概念。
- AI 应用入口。
- 推导深度。
- 实验目标。
- 输出产物。
- 评价方式。
- `dynamic_assets_required`
- `bridge_time_budget`
- `bridge_module_limit`

### 8.2 Profile Contract

原 `teacher_profile.md` 演进为结构化 `profile.yaml`。

`profile.yaml` 最小字段要求：

- `expression_style`
- `lecture_rhythm`
- `boardwork_preference`
- `caution_phrases`
- `avoid_expressions`
- `domain_case_preference`
- `grading_preference`

画像采用两层合并：

- 课程默认画像。
- 教师覆盖画像。

教师画像可影响：

- `Professor Architect Agent`
- 表达与呈现层。

教师画像不得影响：

- 来源可信规则。
- 系统红线。
- 质量门禁。

### 8.3 Lesson Plan Contract

`lesson_plan.yaml` 是主 agent 到所有 subagent 的唯一教学内容源。

每个核心节点必须具备稳定的语义化 `node_id`，并在各产物间保持一致。

核心节点类型固定为：

- `concept`
- `bridge`
- `misconception`
- `experiment`
- `check`
- `homework`
- `conclusion`

每个核心节点至少必须包含：

- 概念内容。
- 补桥模块。
- AI 映射。
- 实验观察点。
- 学生理解证据。
- `source_refs`

每章结果必须稳定回答四个问题：

1. 学生为什么需要学这个数学概念？
2. 这个概念解释了 AI 模型里的哪个关键设计？
3. 学生如何通过实验看到这个数学概念在起作用？
4. 老师如何判断学生是否真正理解，而不是只会背公式？

### 8.4 PPT Contract

PPT 明确采用“富内容讲义型 PPT”，而非极简演讲型 PPT。

`ppt_script.yaml` 最低新增字段：

- `node_id`
- `main_question`
- `key_takeaway`
- `bridge_flag`

`PPT Script Subagent` 负责节点到 slide 的映射。

`ppt_designer` 只执行脚本，不决定教学分页。

### 8.5 Notebook Contract

Notebook 由 `experiment` 节点驱动，而不是整章自由设计。

`notebook_script.yaml` 只能描述：

- 实验目标。
- 代码单元。
- 观察问题。
- 预期现象。

Notebook 与 PPT / lesson plan 默认采用 `node_id` 级对齐。

第一版标准要求为：整本 notebook 端到端可重跑。

### 8.6 Review And Release Contracts

结构化一等公民产物包括：

- `quality_review.yaml`
- `teacher_summary.md`
- `release_manifest.yaml`
- `override.yaml`
- `override_history.yaml`
- `source_proposal.yaml`
- `source_decision.yaml`
- `sources.yaml`
- `sources_catalog.yaml`

所有结构化文件必须带顶层 `schema_version`。

所有治理链产物必须带 `run_id` 与统一时间戳字段。

`run_id` 采用“时间戳 + 短随机后缀”格式，并贯穿所有治理链与发布链。

## 9. Source Governance And Teacher Override

### 9.1 Source Governance

专业内容来源采用“权威来源库 + Agent 生成 + 审查闭环”。

公开来源采用白名单机制，不做无限制动态抓取。

来源治理产物：

- `source_proposal.yaml`
- `source_decision.yaml`
- `sources.yaml`
- `sources_catalog.yaml`

来源 `trust_level` 采用三级制：

- `core`
- `approved`
- `supplemental`

全部核心教学节点必须带 `source_refs`，不得出现无来源核心节点。

当本地来源库缺少足够高可信来源时：

- 默认阻断。
- 提示补源。
- 不得先生成再警告。

### 9.2 Override Governance

`override.yaml` 升级为一等公民产物。

只允许覆盖 `lesson_plan.yaml` 的节点字段，不允许直接覆盖：

- `ppt_script.yaml`
- `quality_review.yaml`
- 系统规则类配置

默认允许覆盖的高频字段包括：

- `main_question`
- `key_takeaway`
- `bridge_toggle`
- `classroom_questions`
- `homework` 相关字段

如 override 触及以下任一条件，必须阻断并复审：

- 红线
- 来源可信链
- 教学主线

override 后默认重审受影响节点；如影响主线、补桥预算或章节红线，则升级为整章复审。

## 10. Quality Gates And Release

### 10.1 Core Gates

所有成品生成前必须通过三重质量门禁：

1. 教学可讲。
2. 数学可信。
3. AI 连接有效。

`quality_review.yaml` 主结构固定为：

1. 红线检查
2. 关键节点结果
3. 维度打分
4. 返工指令

通用评分维度固定为：

- `teachability`
- `trustworthiness`
- `ai_alignment`
- `teacher_relief`

### 10.2 Release Gate

发布门禁固定为：

- 红线全过
- 章节总分达标
- 关键节点全过

第一版高标准门槛固定为：

- 红线全过
- 总分 90+
- 关键节点全过
- 教师 10 分钟内可上课

### 10.3 Run Layout

运行产物根目录采用独立 `outputs/runs`，不与静态配置目录混放。

每章目录下按 `run_id` 保存运行结果。

默认目录分层采用：

- `release/teaching`
- `review/summary`
- `source_bundle`

`teacher_summary.md` 必须每次运行都生成，无论通过还是阻断。

默认路径：

- `review/summary/teacher_summary.md`

`release_manifest.yaml` 为必备产物，至少包含：

- `schema_version`
- `run_id`
- `chapter_id`
- `artifact_list`
- `schema_versions`
- `gate_result`

### 10.4 Source Bundle And Debug

`source_bundle` 必须打包快照，而非只放引用，至少包括：

- `sources`
- `profile`
- `lesson_plan`
- `override`
- `quality_review`
- `release_manifest`
- `source_proposal`
- `source_decision`
- 相关课程与章节配置快照

调试入口采用：

- `source_bundle/debug_index.md`

日志保留在 subagent / skill 任务级，并带 `run_id`。

## 11. Testing And Regression

### 11.1 Golden Samples

第一版至少维护 2 个对比样例：

- 梯度下降
- 概率 / 随机过程类章节

黄金样例回归优先比对结构化中间产物：

- `lesson_plan`
- `ppt_script`
- `quality_review`
- `release_manifest`

最终成品只做存在性与门禁级别检查，不做第一优先级回归基线。

### 11.2 Reuse Tests

用同一套课程 app workflow 迁移到：

- 矩阵与向量空间
- 概率分布与贝叶斯

验收要求：

- 不重写主 agent
- 不改变核心备课流程
- 只替换课程模板和章节配置

### 11.3 Teacher Priority Tests

提供旧 PPT 或讲义时，生成内容必须继承：

- 课程主线
- 术语偏好
- 表达风格
- 章节边界

### 11.4 Knowledge Enhancement Tests

Agent 补充的新案例必须：

- 标注来源或说明依据
- 通过章节匹配审查
- 通过难度审查
- 不覆盖教师核心资料

### 11.5 WeCom End-to-End Tests

企业微信端到端验证至少覆盖：

- 新生成请求
- 状态查询
- 修改请求
- 变更摘要
- 明确确认词
- 按影响范围重生成
- 关键附件回传

### 11.6 Local Deployment Smoke Tests

本机部署 smoke test 至少覆盖：

- WSL2 中 Hermes 可启动
- WeCom adapter 可接收消息
- 本仓库 workflow 可被 Hermes 调用
- 生成结果可写入 `outputs/runs`

## 12. Non-goals And Future Expansion

### 12.1 Non-goals For v1

第一版不做：

- 飞书入口
- 多学科共享入口
- Web 教师工作台
- 通用 Hermes 化
- 个人微信入口
- 无审查的动态外部抓取

### 12.2 Product Boundary

系统是教师备课与复盘副驾驶，不是自动授课系统。

系统应该做：

- 生成结构化备课材料
- 帮助教师把数学抽象和 AI 应用连接起来
- 提供可运行实验和可评价作业
- 沉淀教师课程资产
- 提醒数学严谨性和案例相关性风险

系统不应该做：

- 自动替教师完成课堂现场判断
- 输出无可追溯依据的最新案例
- 为了生成完整文件而牺牲教学逻辑和数学严谨性
- 让主 agent 直接承担所有版式与文件工艺
- 让 subagent 直接输出最终文件
- 让 tool / skill 自行发明教学内容

### 12.3 Future Expansion

后续可扩展方向包括：

- 飞书
- 多学科空间
- Web 审查工作台
- 更多课程模板
- 课程专用 Hermes 发行版 / 封装版

## 13. Open Questions

以下问题尚未锁定，后续应继续讨论：

- 老师自助开通学科空间时，如果自由输入的学科名命中多个模板，系统如何处理。
- 老师自助开通学科空间时，如果输入的学科名没有任何已发布模板，系统如何处理。
- 模板开通成功后，是否在聊天里返回模板版本、学科空间标识和后续可执行动作。
