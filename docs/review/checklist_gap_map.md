# Checklist Gap Map

## Scope Note

- Source of truth remains:
  - `docs/PRD.md`
  - `plans/README.md`
  - `plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md`
- Review input used for this mapping:
  - `D:/Codex_Project/审核清单/Intellectual_Tutor_综合审查清单.md`
- The repository currently does not contain `docs/review/Intellectual_Tutor_综合审查清单.md`; this map therefore treats the external checklist as review input only.
- This document does not change the current resume point, hybrid inference line, or WeCom AI Bot bring-up plan.

## Classification Rules

- `已覆盖`: repo files plus PRD/active plan already make this item true enough for the current stage.
- `部分覆盖`: intent or scaffolding exists, but evidence, runtime validation, or a required sub-capability is still missing.
- `未覆盖`: the checklist asks for something that the repo does not yet materially implement.
- `明确不应纳入当前阶段`: the item conflicts with current v1 boundary or is explicitly deferred by `PRD §12`.

## 已覆盖

- `0.1-1` 方向对，抓住《人工智能数学基础》教师真实痛点
  - 仓库文件: `docs/PRD.md`; `README.md`
  - PRD/Plan: `PRD §1.1-§1.3`
  - 理由: 产品目标、目标教师、教学链条和输出物都围绕 AI 数学基础课程教师的备课痛点定义。
  - 建议归宿: `Reject for now`

- `0.1-2` 系统脑子强，产品定义/架构边界/工作流治理强于普通 AI 课件工具
  - 仓库文件: `AGENTS.md`; `docs/architecture/course-app-overview.md`; `docs/PRD.md`
  - PRD/Plan: `PRD §2`; `PRD §5`; `Plan Fixed Architecture`
  - 理由: 仓库已明确 Agent/Subagent/Tool/Schema 分层，而不是单脚本式“生成课件”。
  - 建议归宿: `Reject for now`

- `0.1-3/0.1-4/0.1-5` 当前仍偏雏形，主要矛盾是落地硬度不足，缺 adoption/信任/验证/托底/组织化能力
  - 仓库文件: `plans/README.md`; `plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md`
  - PRD/Plan: `Plan Current Execution Pointer`; `Plan M7`; `Plan M8`
  - 理由: active plan 已把主 blocker 收敛到 live cloud credentials、WeCom bot validation、repeatable operations，而不是继续堆新功能。
  - 建议归宿: `Reject for now`

- `0.2-1/0.2-2/0.2-4` 系统边界明确、课程层骨架已成、当前仍是可推进样机
  - 仓库文件: `AGENTS.md`; `agents/course-app/*`; `schemas/course/*`; `tools/*`; `outputs/runs/gradient_descent/*`
  - PRD/Plan: `PRD §2`; `PRD §5`; `Plan M1-M6.5`
  - 理由: 骨架、合同、工具、样例 run layout 和 change loop 已经落地，但还未到即插即用产品阶段。
  - 建议归宿: `Reject for now`

- `2.1-1/2.1-2/2.1-3` 坚持 course app 跑在官方 Hermes 上，职责边界清晰，避免膨胀为通用平台
  - 仓库文件: `AGENTS.md`; `docs/architecture/course-app-overview.md`; `docs/deployment/wecom-setup.md`
  - PRD/Plan: `PRD §2`; `PRD §12.1-§12.2`; `Plan Objective`; `Plan Fixed Architecture`
  - 理由: repo 定义、部署文档、non-goals 都反复限制为 official Hermes 上的 course app，而非自造 runtime/memory/gateway。
  - 建议归宿: `Reject for now`

- `2.5-1/2.5-2/2.5-3/2.5-4` 推理分层与风险隔离
  - 仓库文件: `scripts/check_hybrid_inference.py`; `docs/deployment/hermes-wsl2-setup.md`; `configs/hermes/inference_policy.template.yaml`; `agents/course-app/ProfessorArchitectAgent.md`
  - PRD/Plan: `PRD §3.4`; `PRD §5.6`; `Plan Current Execution Pointer`; `Plan M6.5`
  - 理由: local/cloud lane 边界、fallback logging、rules-first routing、local lane 禁区都已写入文档和 smoke-check 工具。
  - 建议归宿: `Reject for now`

- `2.7-3` 是否有统一 run_id、日志、失败原因记录
  - 仓库文件: `tools/run_state.py`; `scripts/generate_chapter.py`; `scripts/check_hybrid_inference.py`
  - PRD/Plan: `PRD §8.6`; `PRD §10.3`; `Plan M5`; `Plan M6.5`
  - 理由: run artifacts、`run_state.yaml`、fallback jsonl 日志和 release manifest 已是固定产物。
  - 建议归宿: `Reject for now`

- `3.6-1` 企业微信只承担发起与通知，而不是深度审阅主界面
  - 仓库文件: `docs/deployment/wecom-setup.md`
  - PRD/Plan: `PRD §7.1`; `PRD §7.4`
  - 理由: PRD 已明确 WeCom 为聊天入口；任务阶段反馈和附件/摘要回传都通过消息通道完成。
  - 建议归宿: `Reject for now`

- `3.13-1/3.13-2` 产品边界与“不做清单”
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §12.1-§12.3`
  - 理由: v1 non-goals 已明写，不做 Web 教师工作台、多学科共享入口、通用 Hermes 化、个人微信入口、无审查动态抓取。
  - 建议归宿: `Reject for now`

- `5.P0-4` 打通一条真实稳定 end-to-end 链路是当前正确主线
  - 仓库文件: `plans/README.md`; `plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md`
  - PRD/Plan: `PRD §4.1`; `PRD §11.5`; `Plan M7`
  - 理由: active plan 已把主线收敛为 cloud credentials + WeCom AI Bot auth + first smoke test。
  - 建议归宿: `Reject for now`

- `6.1-1/6.1-3/6.1-4/6.1-5/6.1-6` 问题定义对、工作流设计对、系统边界健康、治理意识强、方向不是低级 PPT 工具
  - 仓库文件: `AGENTS.md`; `docs/PRD.md`; `docs/architecture/course-app-overview.md`
  - PRD/Plan: `PRD §1-§5`; `Plan M1-M6`
  - 理由: 仓库已经体现为课程级 copilot 和 run-based workflow，而非单一 PPT 生成器。
  - 建议归宿: `Reject for now`

## 部分覆盖

- `0.2-3` 仍未完成真实 end-to-end 稳定闭环
  - 仓库文件: `docs/deployment/wecom-setup.md`; `scripts/check_hybrid_inference.py`
  - PRD/Plan: `PRD §11.5-§11.6`; `Plan M7`; `Plan Immediate Next Slice`
  - 理由: hybrid lane 已通过，但 live cloud-provider 和 WeCom bot message-path 还未闭环。
  - 建议归宿: `Active Plan`

- `1.1-1/1.1-2/1.1-5` 生成包是否少量修改即可上课、是否减少逐页重审、是否真减负
  - 仓库文件: `configs/quality/good_lesson.yaml`; `outputs/runs/gradient_descent/20260424-demo/*`; `scripts/verify_outputs.py`
  - PRD/Plan: `PRD §4.2-§4.4`; `PRD §10.1`; `Plan M5-M6`
  - 理由: repo 有 teacher-quality gate 和黄金样例，但缺真实教师采用证据与稳定课堂使用数据。
  - 建议归宿: `Backlog`

- `1.2-1/1.2-2/1.2-3` 数学可信度、AI 应用桥接自然性、表达是否适合课堂讲授
  - 仓库文件: `configs/quality/good_lesson.yaml`; `sources/chapters/gradient_descent/content.yaml`; `outputs_lecture/*`
  - PRD/Plan: `PRD §4.3`; `PRD §10.1`
  - 理由: 质量门禁和 lecture-handout 样例已存在，但仍是样例级验证，不是跨章节稳定验证。
  - 建议归宿: `Backlog`

- `1.2-4/1.2-5` 区分事实锚点/来源支撑/生成扩展，老师快速判断高置信与必审区
  - 仓库文件: `agents/course-app/SourceCuratorSubagent.md`; `docs/PRD.md`
  - PRD/Plan: `PRD §8.3`; `PRD §9.1`
  - 理由: source governance 规则已写进 PRD 和 subagent brief，但结构化 source artifacts 还没真正落地到 repo。
  - 建议归宿: `Backlog`

- `1.3-1/1.3-2/1.3-3/1.3-4` 公式渲染、细粒度拆解、动态图示、按教师节奏慢讲
  - 仓库文件: `agents/course-app/PPTScriptSubagent.md`; `scripts/verify_outputs.py`; `outputs_lecture/gradient_descent/*`
  - PRD/Plan: `PRD §5.3`; `PRD §8.4`
  - 理由: `formula_spec`、reveal、lecture-handout 样例已存在，但 repo 内没有独立 `formula_renderer` 实现，也无跨章节稳定转换证据。
  - 建议归宿: `Backlog`

- `1.4-1/1.4-2/1.4-3/1.4-4` 符号、变量、解释一致性
  - 仓库文件: `tools/lesson_plan_contracts.py`; `scripts/generate_chapter.py`; `scripts/verify_outputs.py`
  - PRD/Plan: `PRD §8.3-§8.5`; `PRD §10.1`
  - 理由: `node_id` 和结构化合同已在推进跨产物对齐，但没有独立符号表/变量映射审计器。
  - 建议归宿: `Backlog`

- `1.5-1/1.5-2` 是否有真实执行环境、Notebook 是否真实 Run All
  - 仓库文件: `scripts/verify_outputs.py`; `tools/notebook_builder.py`
  - PRD/Plan: `PRD §8.5`; `PRD §11.6`
  - 理由: 当前验证脚本会执行 notebook code cells；但这是 repo 本地执行，不是受控教学沙箱，也还不是 live WeCom/agent 路径下的稳定证据。
  - 建议归宿: `Backlog`

- `1.6-1/1.6-2/1.6-3` 自然语言修改、局部生效、影响范围可见
  - 仓库文件: `scripts/apply_confirmed_change.py`; `tools/change_applier.py`; `tools/run_state.py`
  - PRD/Plan: `PRD §6.2-§6.4`; `Plan M6`
  - 理由: 变更摘要、确认、按 scope 重生成已实现，但影响范围仍主要体现在结构化文件和再生成标志，不是老师可视化层面的“页/实验/产物影响图”。
  - 建议归宿: `Backlog`

- `1.8-1` 明天上课前 20 分钟快速补一页的轻量入口
  - 仓库文件: `docs/deployment/wecom-setup.md`; `scripts/apply_confirmed_change.py`
  - PRD/Plan: `PRD §6`; `PRD §7.5`
  - 理由: WeCom 聊天入口和 change loop 给了轻量路径，但还没有被 live channel 验证为可靠课前微调入口。
  - 建议归宿: `Backlog`

- `2.2-1/2.2-2/2.2-3/2.2-4` 工具层解耦、避免工具偷做决策、structured IO contract
  - 仓库文件: `tools/*`; `scripts/generate_chapter.py`; `scripts/verify_outputs.py`; `schemas/course/*`
  - PRD/Plan: `PRD §5.3-§5.5`; `Plan M2-M3`
  - 理由: 结构化合同和工具文件都存在，但 `tools/verification.py` 仍是 thin wrapper，`generate_chapter.py` 仍直接串 legacy path，解耦还未完成到最终形态。
  - 建议归宿: `Backlog`

- `2.3-1/2.3-2/2.3-3/2.3-4` node_id 锚定、结构抗漂移、严格 scope-aware regeneration、override 后复审
  - 仓库文件: `tools/lesson_plan_contracts.py`; `scripts/apply_confirmed_change.py`; `tools/change_applier.py`
  - PRD/Plan: `PRD §6.4`; `PRD §8.3`; `PRD §9.2`
  - 理由: repo 已用 `node_id`、override、regen scope，但没有 AST / dependency graph 级别的更强锚定，也没有独立复审器。
  - 建议归宿: `Backlog`

- `2.4-4` verification 不仅检查文件生成成功，还检查教学语义一致
  - 仓库文件: `scripts/verify_outputs.py`; `configs/quality/good_lesson.yaml`
  - PRD/Plan: `PRD §10.1`; `PRD §11`
  - 理由: 当前 verification 已超出“文件存在性”，会检查 PPT 内容、notebook 可运行、quality report、source bundle，但还没到独立 cross-artifact semantic auditor。
  - 建议归宿: `Backlog`

- `2.6-1/2.6-2/2.6-3/2.6-4/2.6-5/2.6-6` 失败降级与人工接管
  - 仓库文件: `tools/run_state.py`; `scripts/apply_confirmed_change.py`; `docs/deployment/wecom-setup.md`
  - PRD/Plan: `PRD §7.4`; `PRD §10`; `Plan M8`
  - 理由: repo 有 blocked/released 状态和部分失败后保留产物能力，但没有系统化的“讲稿版/静态实验/缺口报告/人工接管点”实现。
  - 建议归宿: `Backlog`

- `2.7-1/2.7-2/2.7-4` 细粒度状态反馈、阶段展示、debug index/source bundle/review summary
  - 仓库文件: `tools/status_reader.py`; `scripts/read_run_status.py`; `scripts/generate_chapter.py`; `outputs/runs/gradient_descent/*`
  - PRD/Plan: `PRD §7.4`; `PRD §10.3-§10.4`; `Plan M5`
  - 理由: run status、teacher summary、source bundle 已有，但阶段粒度仍粗，`debug_index.md` 仍停留在 PRD 目标而非固定产物。
  - 建议归宿: `Backlog`

- `2.8-2/2.8-3/2.8-4` 部署诊断分层清晰、失败修复路径明确、作者能配出来升级为别人也能稳定配出来
  - 仓库文件: `docs/deployment/hermes-wsl2-setup.md`; `docs/deployment/wecom-setup.md`; `scripts/check_hybrid_inference.py`
  - PRD/Plan: `PRD §3`; `PRD §11.6`; `Plan M8`
  - 理由: 部署文档和 smoke checks 已有，但目前证据仍集中于当前机器和当前操作者。
  - 建议归宿: `Backlog`

- `3.1-1/3.1-2/3.1-3` 第一目标用户聚焦
  - 仓库文件: `docs/PRD.md`; `README.md`
  - PRD/Plan: `PRD §1.3`
  - 理由: PRD 已聚焦 AI 数学基础课程教师，但还未收窄到“刚接手该课的青年老师”这一更尖锐首批用户，也没有据此重写 onboarding/demo。
  - 建议归宿: `Backlog`

- `3.2-1/3.2-2/3.2-3` 第一价值爆点是否锋利
  - 仓库文件: `README.md`; `docs/PRD.md`
  - PRD/Plan: `PRD §1`; `PRD §4`
  - 理由: 当前 repo 同时承载旧课翻新、单章包生成、抽象数学讲清三个价值面，尚未锁成单一首要爆点。
  - 建议归宿: `Backlog`

- `3.3-2/3.3-3` 用户迁移动机与迁移成本
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §1`; `PRD §4`
  - 理由: repo 定义了比普通课件生成更强的系统形态，但没有把“为什么不继续凑合旧 PPT/ChatGPT”写成明确对外表达与低摩擦试用路径。
  - 建议归宿: `Backlog`

- `3.4-1/3.4-2/3.4-3` 首次价值时刻
  - 仓库文件: `outputs/runs/gradient_descent/20260424-demo/*`; `README.md`
  - PRD/Plan: `PRD §4.2`; `PRD §11.1`
  - 理由: 黄金样例存在，但 repo 还没有“输入几项参数即可看到高光片段”的零门槛 demo 入口。
  - 建议归宿: `Backlog`

- `3.7-1/3.7-2/3.7-3` 信任机制外显
  - 仓库文件: `configs/quality/good_lesson.yaml`; `scripts/verify_outputs.py`; `docs/PRD.md`
  - PRD/Plan: `PRD §9`; `PRD §10`
  - 理由: review/source governance/gate 已有规则层，但老师可感知的“来源/风险/责任边界”展示层还没有。
  - 建议归宿: `Backlog`

- `3.9-1/3.9-2/3.9-3` 失败体验设计
  - 仓库文件: `tools/run_state.py`; `docs/deployment/*`
  - PRD/Plan: `PRD §7.4`; `Plan M8`
  - 理由: 当前失败处理更偏工程诊断，还没形成产品化的失败体验与下一步引导。
  - 建议归宿: `Backlog`

- `3.10-1/3.10-2` 课程生命周期覆盖
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §1.1`; `PRD §12.3`
  - 理由: PRD 已声明跨章节连续性和后续课程资产沉淀方向，但 repo 当前验证仍停在单章/单样例。
  - 建议归宿: `Backlog`

- `3.12-3` AI 生成内容、人工修改内容、历史版本是否有审计轨迹
  - 仓库文件: `scripts/apply_confirmed_change.py`; `tools/change_applier.py`; `tools/run_state.py`
  - PRD/Plan: `PRD §8.6`; `PRD §9.2`; `Plan M6`
  - 理由: `run_id`、override、override_history 已提供基础轨迹，但还不是完整权限/版本审计体系。
  - 建议归宿: `Backlog`

- `4.3-1/4.3-2/4.3-3` 责任边界可视化
  - 仓库文件: `docs/PRD.md`; `agents/course-app/SourceCuratorSubagent.md`
  - PRD/Plan: `PRD §2`; `PRD §9`; `PRD §12.2`
  - 理由: docs 层已经明确 source/model/teacher 的责任边界，但尚未变成老师可见的运行期标记与界面。
  - 建议归宿: `Backlog`

- `5.P0-1/5.P0-2/5.P0-6/5.P0-7/5.P0-8` 第一目标用户锁定、第一价值爆点、信任外显、失败降级与人工接管、Notebook 真实执行验证
  - 仓库文件: `docs/PRD.md`; `scripts/verify_outputs.py`; `configs/quality/good_lesson.yaml`
  - PRD/Plan: `PRD §1`; `PRD §8-§10`; `PRD §11.6`
  - 理由: 方向已写入，但仍缺更硬的 runtime 证据或更窄的产品表达。
  - 建议归宿: `Backlog`

- `5.P1-1/5.P1-2/5.P1-3/5.P1-4/5.P1-5/5.P1-6` auditor、教学风险矩阵、安装成功率体系、课堂反馈回流、教师控制旋钮、资产权限/团队协作
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §8-§12`; `Plan M8`
  - 理由: PRD 已提出部分方向，但 repo 尚无系统化落地。
  - 建议归宿: `Backlog`

- `6.1-2` 目标用户方向基本对
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §1.3`
  - 理由: 已聚焦大学 AI 数学基础课程教师，但还可以更尖锐。
  - 建议归宿: `Backlog`

- `6.2-1/6.2-2/6.2-3/6.2-4/6.2-5/6.2-6/6.2-7/6.2-8` 当前最缺的八项
  - 仓库文件: `docs/PRD.md`; `plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md`
  - PRD/Plan: `PRD §11-§12`; `Plan M7-M8`
  - 理由: 这八项基本都对应 backlog 主题，且与当前主 blocker 解掉后的下一阶段建设直接相关。
  - 建议归宿: `Backlog`

- `6.3-1/6.3-2` 一句话总判断：方向对，但胜负手在验证/托底/信任/控制感/审阅体验/组织化能力
  - 仓库文件: `plans/README.md`; `plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md`
  - PRD/Plan: `Plan Current live blocker`; `Plan M8`
  - 理由: 与当前 repo 和 active plan 事实一致，但仍需在 blocker 解掉后吸收到更长期 backlog。
  - 建议归宿: `Backlog`

## 未覆盖

- `1.1-3/1.1-4` 量化节省备课时间、量化手工修改/返工/采用率
  - 仓库文件: none
  - PRD/Plan: not yet explicit beyond `PRD §12.3` future direction
  - 理由: repo 没有 adoption metrics、teacher-relief telemetry 或 sample study 设计。
  - 建议归宿: `Backlog`

- `1.5-3/1.5-4` 实验失败时自动给最小替代方案、课堂网络/环境差时保底方案
  - 仓库文件: none
  - PRD/Plan: only implied by `PRD §10`; not planned explicitly
  - 理由: 当前 notebook verification 只能验证成功路径，不能自动产出降级版本。
  - 建议归宿: `Backlog`

- `1.6-4` 课前 10 分钟内完成小范围微调的验证证据
  - 仓库文件: none
  - PRD/Plan: not yet explicit
  - 理由: repo 还没有任务时长 SLA、teacher-facing quick-edit flow 或 smoke script。
  - 建议归宿: `Backlog`

- `1.7-1/1.7-2/1.7-3` 课堂与课后反馈闭环
  - 仓库文件: none
  - PRD/Plan: only future intent in `PRD §1.1`
  - 理由: 没有 `class_feedback` 类结构化合同，没有回流到 profile/lesson plan/next chapter 的实现。
  - 建议归宿: `Backlog`

- `1.8-2/1.8-3` 复习课/补课/压缩课时/不同班型切换
  - 仓库文件: none
  - PRD/Plan: not explicitly implemented
  - 理由: 当前 chapter config 没有多班型或压缩版组织机制。
  - 建议归宿: `Backlog`

- `2.4-1/2.4-2/2.4-3` 独立 cross-artifact consistency auditor、node_id 覆盖率/符号表/变量映射审计、PPT/Notebook/DOCX/作业语义对齐校验
  - 仓库文件: none
  - PRD/Plan: desired in `PRD §8-§10`; absent from active milestone deliverables
  - 理由: 当前只有 verification checks，没有独立一致性审计层。
  - 建议归宿: `Backlog`

- `2.7-4` debug index
  - 仓库文件: none
  - PRD/Plan: `PRD §10.4`
  - 理由: `source_bundle` 和 summary 已有，但 `debug_index.md` 还没成为固定产物。
  - 建议归宿: `Backlog`

- `2.8-1` 一键自检 / 安装向导 / 红黄绿状态盘
  - 仓库文件: none
  - PRD/Plan: `PRD §11.6`; `Plan M8`
  - 理由: 当前是文档 + smoke script，尚无整合 operator self-check。
  - 建议归宿: `Backlog`

- `2.9-1/2.9-2/2.9-3/2.9-4` 教学风险测试矩阵
  - 仓库文件: none
  - PRD/Plan: `PRD §11.1-§11.4`
  - 理由: PRD 写了 test intent，但 repo 还没有 matrix、fixture 套件和多章节回归。
  - 建议归宿: `Backlog`

- `3.3-1` 系统化替代品比较
  - 仓库文件: none
  - PRD/Plan: none explicit
  - 理由: 没有把旧 PPT、同事资料、ChatGPT/Claude 零散补、手工拼教材做成对比式定位文档。
  - 建议归宿: `Backlog`

- `3.5-1/3.5-2/3.5-3` 旧资产导入
  - 仓库文件: none
  - PRD/Plan: not yet scoped
  - 理由: 当前输入仍是 repo 内结构化 source files，不支持拖拽旧 PPT/PDF/Word/手写草稿。
  - 建议归宿: `Backlog`

- `3.7-1/3.7-2/3.7-3` 以老师可理解界面外显来源/review/风险/责任
  - 仓库文件: none
  - PRD/Plan: intended by `PRD §9-§10`
  - 理由: 规则存在，老师可感知层不存在。
  - 建议归宿: `Backlog`

- `3.8-1/3.8-2/3.8-3` 教师控制感：保守/激进、保留原稿、标出新增/改写/继承
  - 仓库文件: none
  - PRD/Plan: not explicitly implemented
  - 理由: 当前只有 change request/confirmation，没有控制旋钮和 lineage 标记。
  - 建议归宿: `Backlog`

- `4.1-1/4.1-2/4.1-3` 教学结果归因模型
  - 仓库文件: none
  - PRD/Plan: none explicit
  - 理由: repo 没有 `class_feedback`、`teaching_outcome`、`node_effectiveness` 之类合同。
  - 建议归宿: `Backlog`

- `4.2-1/4.2-2` 日程流与运营流设计
  - 仓库文件: none
  - PRD/Plan: none explicit
  - 理由: repo 当前只覆盖生成/修改/review/release，不覆盖“本周讲什么/哪个班讲到哪”的运营层。
  - 建议归宿: `Backlog`

- `5.P0-3/5.P0-5` 零门槛 demo 入口、最小教师审阅台
  - 仓库文件: none
  - PRD/Plan: currently outside active M7 bring-up
  - 理由: 样例和 artifacts 已有，但缺单独 demo flow；教师审阅台更是未落地。
  - 建议归宿: `Backlog`

- `5.P2-1/5.P2-2/5.P2-4` 生命周期闭环、团队协作与课程资产升级、量化减负与教学效果指标
  - 仓库文件: none
  - PRD/Plan: future direction only
  - 理由: 这些方向尚未进入 repo implementation。
  - 建议归宿: `Backlog`

- `6.1-?` 注：Section 6 的“最缺什么”中涉及的 teacher trust / attribution / org use 等项，若未在上方单列，均应按对应 backlog 主题处理
  - 仓库文件: none
  - PRD/Plan: synthesized from `PRD §11-§12`
  - 理由: 这是对前面缺口的总结性复述，不形成新的 source of truth。
  - 建议归宿: `Backlog`

## 明确不应纳入当前阶段

- `2.10-1/2.10-2` 从单机到组织部署的迁移路线、为组织化使用预留完整权限/日志/资产管理空间
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §3.1`; `PRD §12.1`; `PRD §12.3`
  - 理由: 当前部署范围被明确限定为当前 Windows + WSL2 + 单 course-focused Hermes instance；组织化路线属于 future expansion。
  - 建议归宿: `Reject for now`

- `3.6-2/3.6-3` 最小 Web 审阅台、老师可视化审阅界面
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §7.1`; `PRD §12.1`; `PRD §12.3`
  - 理由: `PRD §12.1` 明写 v1 不做 `Web 教师工作台`；当前主入口固定为 WeCom。
  - 建议归宿: `Reject for now`

- `3.11-1/3.11-2/3.11-3/3.11-4` 教学团队协作与课程组资产沉淀机制
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §7.2`; `PRD §12.3`
  - 理由: 当前 v1 固定为单学科、单入口、单老师当前这门课的主 agent；团队版能力属于后续扩展。
  - 建议归宿: `Reject for now`

- `3.12-1/3.12-2` 个人/团队/学校公共资产权限与版权边界
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §3.1`; `PRD §12.3`
  - 理由: 当前是单机 bring-up 验证，不是多主体资产平台。
  - 建议归宿: `Reject for now`

- `3.14-1/3.14-2/3.14-3` 传播与增长设计
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §12.3`
  - 理由: 当前仓库主线是 hybrid inference + WeCom bring-up，不是 demo marketing / virality system。
  - 建议归宿: `Reject for now`

- `4.4-1/4.4-2` 组织化使用迁移路线
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §3.1`; `PRD §12.3`
  - 理由: 与 `2.10` 同类，属于 future expansion，不应打断当前单机 v1 验证主线。
  - 建议归宿: `Reject for now`

- `5.P2-3/5.P2-5` 从单机部署走向组织化使用的迁移路线、传播与增长设计
  - 仓库文件: `docs/PRD.md`
  - PRD/Plan: `PRD §12.3`
  - 理由: 属于未来扩展，不应在当前 blocker 未解时进入主规划。
  - 建议归宿: `Reject for now`

## Notes For Mainline Protection

- 当前最不该被打断的主线是：
  - `Plan M7`: live cloud credentials
  - `Plan M7`: WeCom AI Bot authentication
  - `PRD §11.5-§11.6`: first e2e smoke evidence
- 当前最值得在 blocker 解掉后再吸收到主规划的主题是：
  - cross-artifact auditor
  - notebook failure fallback
  - deployment/operator self-check
  - teacher trust surface
  - first user / first value spike narrowing
