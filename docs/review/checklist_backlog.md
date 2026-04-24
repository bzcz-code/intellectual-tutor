# Checklist Backlog

## Scope Note

- This backlog is derived only from items classified as `部分覆盖` or `未覆盖` in `docs/review/checklist_gap_map.md`.
- It does not modify:
  - `docs/PRD.md`
  - `plans/README.md`
  - `plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md`
- The current mainline remains:
  - keep hybrid local/cloud lane stable
  - provide live cloud-provider credentials
  - complete WeCom AI Bot authentication and first smoke test

## P0

### 1. Live WeCom E2E Acceptance Evidence

- Checklist refs:
  - `0.2-3`
  - `2.8-2/2.8-3`
  - `5.P0-4`
- 为什么重要:
  - 当前主线最终验收仍依赖 live cloud lane + WeCom AI Bot message path。
  - 没有这组证据，仓库仍只能被视为“样机已搭好”，不能视为 v1 bring-up 通过。
- 为什么现在不一定立刻做:
  - 它本身就是当前 active implementation plan 的最后一段，不需要另起新规划文件。
  - 本轮目标是审查映射和 backlog 分流，不是改主规划。
- 推荐归属:
  - `future implementation plan`

### 2. Operator Self-Check And Layered Diagnostics

- Checklist refs:
  - `2.8-1/2.8-2/2.8-3/2.8-4`
  - `5.P1-3`
- 为什么重要:
  - 当前 bring-up 依赖多层环境：Windows `Ollama`、`WSL2`、Hermes、cloud provider、WeCom。
  - 如果没有统一 operator self-check，后续验收质量和重复部署成功率都不稳。
- 为什么现在不一定立刻做:
  - 在 live WeCom smoke test 通过前，做完整自检工具容易把注意力从主 blocker 转移到工具化包装。
- 推荐归属:
  - `future implementation plan`

### 3. Notebook Classroom-Safe Verification And Fallback

- Checklist refs:
  - `1.5-1/1.5-2/1.5-3/1.5-4`
  - `5.P0-8`
- 为什么重要:
  - notebook 是课堂风险最高的交付件之一；仅有成功路径验证不足以支撑“敢上课”。
  - 失败 fallback 直接影响课堂可用性和老师信任。
- 为什么现在不一定立刻做:
  - 当前 repo 已有 `Run All` 级验证，先完成主线 bring-up 后再补“失败时也可用”的保底层更稳。
- 推荐归属:
  - `future implementation plan`

### 4. Minimal Failure Downgrade And Human Handoff Contract

- Checklist refs:
  - `2.6-1/2.6-2/2.6-3/2.6-4/2.6-5/2.6-6`
  - `3.9-1/3.9-2/3.9-3`
  - `5.P0-7`
- 为什么重要:
  - 当前系统已经有 blocked/released 状态，但还没有系统化的“失败后老师继续工作”能力。
  - 这直接影响当前主线验收的可靠性和老师是否信任 bot 回复。
- 为什么现在不一定立刻做:
  - 必须先知道 live WeCom path 的真实失败形态，再决定最小降级包长什么样。
- 推荐归属:
  - `PRD append`

### 5. Minimal Cross-Artifact Acceptance Gate

- Checklist refs:
  - `1.4-1/1.4-2/1.4-3/1.4-4`
  - `2.4-1/2.4-2/2.4-3/2.4-4`
  - `5.P1-1`
- 为什么重要:
  - 当前 release gate 已有，但还不足以证明 PPT/DOCX/IPYNB/作业在语义上真正对齐。
  - 这是验收质量问题，不只是未来优化问题。
- 为什么现在不一定立刻做:
  - 在 current blocker 未解时，先做 full auditor 容易演变成第二条主线。
  - 更合理的是先定义最小 acceptance gate，再在下一阶段扩展。
- 推荐归属:
  - `future implementation plan`

### 6. Teacher-Facing Status And Impact Visibility

- Checklist refs:
  - `1.6-1/1.6-2/1.6-3`
  - `2.7-1/2.7-2/2.7-4`
  - `5.P0-6`
- 为什么重要:
  - 当前已有 run state、summary、override，但老师可感知的“当前在做什么、这次改动影响什么”还不够外显。
  - 这直接影响当前 WeCom 交互的可理解性和验收体验。
- 为什么现在不一定立刻做:
  - 应先用 live bot bring-up 暴露真实交互缺口，再决定最小需要补到聊天里还是后续工作台里。
- 推荐归属:
  - `PRD append`

## P1

### 7. First User Narrowing And First Value Spike Lock

- Checklist refs:
  - `3.1-1/3.1-2/3.1-3`
  - `3.2-1/3.2-2/3.2-3`
  - `5.P0-1/5.P0-2`
- 为什么重要:
  - 仓库已经知道“服务谁”，但还没锁成最尖锐的首批用户和唯一第一爆点。
  - 没有这个收口，后续 PRD 会继续同时承担多个价值主张。
- 为什么现在不一定立刻做:
  - 这属于 blocker 解掉后的产品收口，不是当前部署 bring-up 的前置条件。
- 推荐归属:
  - `PRD append`

### 8. Zero-Threshold Demo And Aha-Moment Path

- Checklist refs:
  - `3.4-1/3.4-2/3.4-3`
  - `5.P0-3`
- 为什么重要:
  - 当前黄金样例已经存在，但缺少一条给新老师快速感知价值的 demo 路径。
  - 它会影响 adoption，而不是只影响文档美观。
- 为什么现在不一定立刻做:
  - 在 live channel 未打通前做 demo 包装，容易掩盖 runtime 风险。
- 推荐归属:
  - `future implementation plan`

### 9. Source Governance Artifacts From PRD To Repo

- Checklist refs:
  - `1.2-4/1.2-5`
  - `4.3-1/4.3-2/4.3-3`
- 为什么重要:
  - PRD 已经把 source governance 写得很重，但 repo 还没有 `source_proposal.yaml` / `source_decision.yaml` / `sources.yaml` / `sources_catalog.yaml`。
  - 这会造成 PRD 和仓库实现之间的漂移。
- 为什么现在不一定立刻做:
  - 当前 blocker 更靠近 deployment/e2e；source governance artifacts 的增补适合在主线通过后一次性补齐。
- 推荐归属:
  - `future implementation plan`

### 10. Structured Profile Contract Migration

- Checklist refs:
  - `1.7-2`
  - `3.8-1/3.8-2/3.8-3`
  - related PRD drift around `profile.yaml`
- 为什么重要:
  - PRD 已经写成 `profile.yaml`，但 repo 仍使用 `profiles/teacher_profile.md`。
  - 这是典型文档-实现漂移点，后续会影响 teacher preference 沉淀和控制感设计。
- 为什么现在不一定立刻做:
  - 不会直接阻塞当前 hybrid/WeCom bring-up；更适合作为 blocker 后的结构对齐工作。
- 推荐归属:
  - `future implementation plan`

### 11. Teaching-Risk Regression Matrix

- Checklist refs:
  - `2.9-1/2.9-2/2.9-3/2.9-4`
  - `5.P1-2`
- 为什么重要:
  - 当前只有 `gradient_descent` 黄金样例，不足以覆盖高风险数学章节、应用桥接章节、旧课翻新、多轮修改等教学风险。
- 为什么现在不一定立刻做:
  - 在主线 message-path 未打通前，补大量 regression fixtures 的回报不如先完成端到端证据。
- 推荐归属:
  - `future implementation plan`

### 12. Teacher Trust Surface

- Checklist refs:
  - `3.7-1/3.7-2/3.7-3`
  - `5.P0-6`
- 为什么重要:
  - 当前 repo 有 review、gate、source governance 规则，但老师看不见它们如何影响当前输出。
  - 这会直接削弱 adoption。
- 为什么现在不一定立刻做:
  - 需要先观察 live WeCom 交互的最小可承载信息量，再决定哪些 trust signals 该先进聊天，哪些留给后续审阅层。
- 推荐归属:
  - `PRD append`

### 13. Feedback Loop And Teaching Outcome Attribution

- Checklist refs:
  - `1.7-1/1.7-2/1.7-3`
  - `4.1-1/4.1-2/4.1-3`
  - `5.P1-4`
- 为什么重要:
  - 没有课后反馈回流和 outcome attribution，系统就无法从“生成工具”升级到“课程资产改进系统”。
- 为什么现在不一定立刻做:
  - 需要先有 live usage path，再设计最小反馈合同，否则只能空转写 schema。
- 推荐归属:
  - `research note`

### 14. Teacher Control Knobs And Revision Lineage

- Checklist refs:
  - `3.8-1/3.8-2/3.8-3`
  - `5.P1-5`
- 为什么重要:
  - 当前 change flow 有确认，但没有“尽量保留原稿/只补案例/只增强实验”等控制旋钮，也没有新增/改写/继承标记。
- 为什么现在不一定立刻做:
  - 需要先从真实 teacher change requests 看最常见控制模式，再定 knobs。
- 推荐归属:
  - `PRD append`

## P2

### 15. Alternative Comparison And Migration Story

- Checklist refs:
  - `3.3-1/3.3-2/3.3-3`
- 为什么重要:
  - adoption 不只取决于功能强，还取决于是否回答了“为什么不继续凑合旧方案”。
- 为什么现在不一定立刻做:
  - 它不会阻塞当前部署主线，更适合在 e2e 打通后做成产品叙事与研究材料。
- 推荐归属:
  - `research note`

### 16. Legacy Asset Import Path

- Checklist refs:
  - `3.5-1/3.5-2/3.5-3`
- 为什么重要:
  - 旧 PPT/PDF/Word 导入能力是老师真实迁移路径的关键。
- 为什么现在不一定立刻做:
  - 这是独立子系统，容易把当前 repo 从“验证工作流”拉向“文档摄取平台”。
- 推荐归属:
  - `future implementation plan`

### 17. Class-Schedule And Operations Layer

- Checklist refs:
  - `1.8-2/1.8-3`
  - `4.2-1/4.2-2`
- 为什么重要:
  - 真实教学运行不是单次任务，而是排课、补课、压缩、进度同步。
- 为什么现在不一定立刻做:
  - 当前 v1 仍以单章闭环验证为主，运营层会引入新的状态管理复杂度。
- 推荐归属:
  - `research note`

### 18. Full Course Lifecycle Coverage

- Checklist refs:
  - `3.10-1/3.10-2`
  - `5.P2-1`
- 为什么重要:
  - 这是从“单章工具”跨向“课程 copilot”的核心跃迁。
- 为什么现在不一定立刻做:
  - 需要先把单章闭环和 live channel 做扎实，再扩到开课前/课中/课后/期中/归档。
- 推荐归属:
  - `future implementation plan`

### 19. Team Collaboration And Asset Governance

- Checklist refs:
  - `3.12-3`
  - related collaboration/governance themes after single-machine v1
- 为什么重要:
  - 一旦进入课程组协作，版本审计、ownership、asset lineage 都会变成基础能力。
- 为什么现在不一定立刻做:
  - 当前 v1 明确不是多主体资产平台，这些能力在 blocker 解掉前投入产出比低。
- 推荐归属:
  - `research note`

### 20. Quantified Teacher Relief And Learning Outcome Metrics

- Checklist refs:
  - `1.1-3/1.1-4`
  - `5.P2-4`
- 为什么重要:
  - 这是未来判断“是否真的减负、是否真的值得推荐”的硬指标。
- 为什么现在不一定立刻做:
  - 指标体系需要真实用户和真实课堂数据，当前仓库还处于 bring-up 阶段。
- 推荐归属:
  - `research note`

## Hold Until Current Blocker Is Cleared

- 不该打断当前主线、但已经值得盯住的:
  - `P0-2` operator self-check
  - `P0-3` notebook fallback
  - `P0-4` failure downgrade/handoff
  - `P0-5` minimal cross-artifact acceptance gate
  - `P0-6` teacher-facing status/impact visibility
- 适合在 current blocker 解掉后吸收到主规划中的:
  - `P1-7` first user narrowing
  - `P1-9` source governance artifacts
  - `P1-10` profile contract migration
  - `P1-11` teaching-risk regression matrix
  - `P1-12` teacher trust surface
