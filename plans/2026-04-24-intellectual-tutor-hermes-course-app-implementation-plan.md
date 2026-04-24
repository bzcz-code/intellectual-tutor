# Intellectual Tutor Hermes Course App Implementation Plan

## Objective

Upgrade `D:\Codex_Project\intellectual_tutor` from a local single-chapter generation repository into:

- a course-prep app that runs on top of the official `Hermes Agent`
- a course instance that uses the official `WeCom` callback adapter as the teacher entry point
- a v1 teacher loop covering generate package, query status, propose change, explicit confirmation, and regeneration

This plan explicitly rejects the earlier wrong route of building a separate Hermes runtime, memory system, or messaging gateway inside this repository.

## Current Execution Pointer

The repository-side course-app scaffolding is already in place.

When continuing this plan, do not restart from early repo-internal scaffolding tasks or from initial WSL2/Hermes installation unless the machine has been reset.

The next execution slice is:

1. implement the approved hybrid local/cloud inference policy in docs, templates, and runtime wiring
2. install and validate `Ollama` inside `WSL2` for the dedicated Hermes instance
3. use `gemma4` as the local low-cost lane for:
   simple questions, status explanations, fixed-format helper drafts, and candidate run summaries
4. keep official Hermes memory, `memory` tool, and `session_search` as the only built-in memory/summary path
5. keep a live cloud provider for:
   `Professor Architect Agent`, core subagent generation, `quality_review`, source governance, and release gating
6. auto-upgrade local failures or uncertainty to the cloud lane and log the local miss
7. after the hybrid lane is validated, continue with live cloud credentials and WeCom callback secrets in `$HERMES_HOME/.env`
8. resume the WeCom callback endpoint validation and end-to-end smoke test

Current default resume point:

1. open `Ubuntu-24.04` in `WSL2` as `root`
2. export `HERMES_HOME=/root/.hermes-intellectual-tutor`
3. verify `ollama.service` is running and retry `ollama pull gemma4:e4b`
4. stop only when `ollama list` shows `gemma4:e4b`
5. run the repo-side smoke check:
   `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor`
6. if that passes, move directly into `$HERMES_HOME/.env` cloud-provider and WeCom secret configuration

Primary references:

- `docs/PRD.md`
- `docs/deployment/hermes-wsl2-setup.md`
- `docs/deployment/wecom-setup.md`
- `scripts/bootstrap_hermes_course_app.py`

Rule for new sessions:

- If the user says "continue the plan" or "继续完成计划", start from hybrid routing implementation on top of the existing WSL2 Hermes install.
- Do not restart from M1 document scaffolding unless files are missing.

## Execution Update 2026-04-24

Completed in prior execution:

- installed `WSL2` distro `Ubuntu-24.04`
- verified `WSL2` entry with `root`, kernel visibility, and repo mount at `/mnt/d/Codex_Project/intellectual_tutor`
- installed the official `Hermes Agent` into `/root/.hermes-intellectual-tutor/hermes-agent`
- initialized dedicated `HERMES_HOME=/root/.hermes-intellectual-tutor`
- ran `scripts/bootstrap_hermes_course_app.py` inside `WSL2`
- verified `config.yaml` contains `skills.external_dirs: /mnt/d/Codex_Project/intellectual_tutor/skills`
- verified Hermes can see the repo skill `intellectual-tutor-course-workflow`

Completed in this session:

- confirmed with the user that cost control should use a hybrid inference split
- fixed the local deployment target to `Ollama` inside the same `WSL2` environment as the dedicated Hermes instance
- fixed the default local model target to `gemma4`
- fixed the first local lane scope to:
  simple questions, status explanations, fixed-format helper drafts, and candidate run summaries
- fixed the fallback rule to:
  auto-upgrade local failures or uncertainty to the cloud lane and log the local miss
- fixed the summary/memory rule to:
  keep official Hermes `memory` and `session_search` as the only built-in memory path, with no repo-local clone
- rewrote the opening of `docs/PRD.md` to state the final product goal, core use scenarios, and core product functions explicitly, so new sessions do not read the repo as only a vague single-chapter generator
- aligned the root `README.md` opening summary with the updated PRD so the repository entry point now states the final product as a teacher copilot with WeCom entry, dialogue revision, confirmed preference learning, and cross-chapter continuity
- pushed the hybrid-routing boundary into the runtime-facing repo files:
  `configs/hermes/SOUL.template.md`, `agents/course-app/ProfessorArchitectAgent.md`, and `skills/course/intellectual-tutor-course-workflow/SKILL.md`
- added `configs/hermes/inference_policy.template.yaml` and updated `scripts/bootstrap_hermes_course_app.py` to materialize it into the dedicated `HERMES_HOME`
- added `scripts/check_hybrid_inference.py` so the local lane and fallback-log behavior can be smoke-tested from `WSL2`
- updated `docs/deployment/hermes-wsl2-setup.md` with the repo-specific `Ollama` install and hybrid-lane verification steps
- bootstrapped `/root/.hermes-intellectual-tutor` again so the live instance now includes:
  `SOUL.md` with routing policy and `intellectual_tutor_inference_policy.yaml`
- installed `Ollama 0.21.1` inside `Ubuntu-24.04`, created `/etc/systemd/system/ollama.service`, and verified the service binds `127.0.0.1:11434`
- initialized `AGENT.md` and rewrote `AGENTS.md` so both now point at the current plan-driven resume workflow instead of the earlier stale WSL2/Hermes install pointer
- expanded `AGENTS.md` into a real repository orientation document with:
  read order, layered project map, key entry scripts, key Hermes tools, task-to-file routing, and the default concrete example path under `gradient_descent`
- retried `ollama pull gemma4:e4b` from the dedicated `Ubuntu-24.04` runtime; the pull now gets past manifest resolution and starts a 16-part blob download, but still exits before completion
- captured `journalctl` evidence showing repeated `EOF`, `unexpected EOF`, and intermittent `dial tcp 198.18.0.201/202:443: i/o timeout` while downloading blob `sha256:4c27e0f5b5ad...`
- verified with `curl -Ivs` from `WSL2` that both `https://registry.ollama.ai/v2/` and the signed `r2.cloudflarestorage.com` blob host are TLS-reachable, so the blocker is large-transfer stability rather than basic DNS or certificate failure
- verified that `ollama list` remains empty while partial blob files are accumulating under `/usr/share/ollama/.ollama/models/blobs/`

Remaining work:

- validate `gemma4:e4b` pull completion in `WSL2`
- run `scripts/check_hybrid_inference.py` against the dedicated `HERMES_HOME`
- verify automatic fallback logging
- configure live cloud-provider access in `$HERMES_HOME/.env`
- configure WeCom callback secrets in `$HERMES_HOME/.env`
- start the Hermes gateway and verify callback binding
- run the first allowed-user WeCom smoke test
- capture callback and smoke-test evidence for later handoff

Current blockers and assumptions:

- the hybrid routing design is now wired into repo templates and smoke-check tooling, but the first local-model pull is not complete yet
- a live cloud provider is still required for high-risk teaching tasks even after the local lane is added
- the local lane must stay outside `lesson_plan`, `quality_review`, source governance, and release gating
- official Hermes memory behavior remains the source of truth for long-term summaries and session recall
- the dedicated runtime should continue using `/root/.hermes-intellectual-tutor` unless the machine setup changes
- current blocker on the machine:
  `ollama pull gemma4:e4b` now gets past manifest resolution and starts downloading blob
  `sha256:4c27e0f5b5adf02ac956c7322bd2ee7636fe3f45a8512c9aba5385242cb6e09a`,
  but the transfer repeatedly fails with `EOF`, `unexpected EOF`, and intermittent
  `dial tcp 198.18.0.201/202:443: i/o timeout`
- `curl -Ivs` confirms both the registry host and the signed Cloudflare blob host are reachable from `WSL2`, so the active issue is sustained large-blob transfer stability rather than basic host reachability
- `ollama list` is still empty and partial blob files remain under `/usr/share/ollama/.ollama/models/blobs/`
- until `ollama list` shows `gemma4:e4b`, do not advance to `.env` credential wiring or WeCom callback validation

Verification evidence already captured:

- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'whoami && uname -a && python3 --version'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash -s -- --skip-setup --hermes-home /root/.hermes-intellectual-tutor'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; /root/.hermes-intellectual-tutor/hermes-agent/venv/bin/python /mnt/d/Codex_Project/intellectual_tutor/scripts/bootstrap_hermes_course_app.py --hermes-home /root/.hermes-intellectual-tutor'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; /root/.local/bin/hermes skills list'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; /root/.local/bin/hermes doctor'`
- `python -m py_compile scripts/bootstrap_hermes_course_app.py scripts/check_hybrid_inference.py`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'cd /mnt/d/Codex_Project/intellectual_tutor && python3 scripts/bootstrap_hermes_course_app.py --hermes-home /root/.hermes-intellectual-tutor --overwrite-soul'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'curl -fsSL https://ollama.com/install.sh | sh'` followed by the explicit install/retry path with `zstd`, service creation, and `systemctl enable ollama`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'curl -fsS http://127.0.0.1:11434/api/tags'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'journalctl -u ollama -n 80 --no-pager'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; /usr/local/bin/ollama pull gemma4:e4b'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'journalctl -u ollama -n 120 --no-pager'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'env | grep -i proxy || true; getent ahosts registry.ollama.ai || true; timeout 20 curl -Ivs https://registry.ollama.ai/v2/ 2>&1 || true'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'getent ahosts dd20bb891979d25aebc8bec07b2b3bbc.r2.cloudflarestorage.com || true; timeout 20 curl -Ivs https://dd20bb891979d25aebc8bec07b2b3bbc.r2.cloudflarestorage.com 2>&1 || true'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'ls -lah /usr/share/ollama/.ollama/models; find /usr/share/ollama/.ollama/models/blobs -maxdepth 1 -type f | sed -n "1,40p"'`

## Progress Synchronization Protocol

This plan is the repository source of truth for execution status.

After every meaningful task batch, update this file before ending the session.

Each update should capture:

1. current milestone state
2. completed work
3. remaining work
4. exact next step
5. blockers, assumptions, or environment prerequisites
6. verification commands or evidence when relevant

If the resume point changes, also update:

- `plans/README.md`
- `README.md`
- `docs/README.md`

Do not rely on chat history as the only handoff mechanism.

## Current Milestone Snapshot

- `M1 Hermes Integration Skeleton`: completed in repo
- `M2 Workflow Contract Refactor`: completed in repo
- `M3 Toolization Of Existing Generators`: completed in repo
- `M4 Course Agent And Subagent Setup`: repo-side skeleton completed
- `M5 Run Layout And Release Chain`: completed for local run-based workflow
- `M6 Teacher Change Loop`: completed for local workflow, including structured and legacy compatibility plus PPT regeneration sync
- `M6.5 Hybrid Inference Cost-Control Lane`: repo-side implementation is in place, but live `gemma4:e4b` availability and smoke-test evidence are still blocked on the WSL2 model pull
- `M7 WeCom End-to-End Integration`: in progress; WSL2 distro, official Hermes install, dedicated `HERMES_HOME`, repo-skill mounting, and repo-side hybrid-routing wiring are verified, but live local-model validation, callback secrets, and message-path testing are still pending
- `M8 Regression And Local Operations`: partially prepared in docs and in the live machine environment, but not completed as a verified deployed system

## Fixed Architecture

### Official Hermes Core

External to this repository:

- memory, summary, and cleanup mechanisms
- session and adapter framework
- agent runtime
- tool calling and subagent orchestration

### Intellectual Tutor Course App

Owned by this repository:

- course agent and subagent prompts
- workflow contracts
- chapter generation and review tools
- WeCom deployment guidance
- local WSL2 deployment guidance
- inference routing policy for local vs cloud lanes

### WeCom Entry

The first version uses the official Hermes `WeCom` adapter directly. This repo does not implement a custom chat gateway.

### Hybrid Inference Lane

The approved cost-control lane is:

- official Hermes memory, `memory` tool, and `session_search` remain the built-in summary and recall system
- local `Ollama + gemma4` in `WSL2` serves low-risk requests
- a live cloud provider remains required for high-risk teaching generation and review

## Milestones

### M1. Hermes Integration Skeleton

Goal: define the repository as a Hermes-loadable course app instead of a standalone script runner.

Delivered:

- `docs/deployment/hermes-wsl2-setup.md`
- `docs/deployment/wecom-setup.md`
- `docs/architecture/course-app-overview.md`
- `configs/hermes/` templates
- `skills/` course skill skeleton
- `agents/` course prompt skeleton

### M2. Workflow Contract Refactor

Goal: express the chapter workflow through structured contracts instead of informal script coupling.

Delivered:

- `schemas/course/lesson_plan.yaml`
- `schemas/course/ppt_script.yaml`
- `schemas/course/notebook_script.yaml`
- `schemas/course/quality_review.yaml`
- `schemas/course/release_manifest.yaml`
- `schemas/course/change_request.yaml`
- `schemas/course/change_confirmation.yaml`

### M3. Toolization Of Existing Generators

Goal: refactor the existing Python generation path into Hermes-callable course tools.

Delivered:

- `tools/lesson_plan_builder.py`
- `tools/ppt_designer.py`
- `tools/notebook_builder.py`
- `tools/verification.py`
- `tools/release_packager.py`
- `tools/status_reader.py`
- `tools/change_applier.py`

### M4. Course Agent And Subagent Setup

Goal: define the course workflow as a Hermes agent system with clear role boundaries.

Delivered:

- course persona and prompt structure
- `Professor Architect Agent`
- `PPT Script Subagent`
- `Notebook Lab Subagent`
- `Quality Review Subagent`
- `Source Curator Subagent`

### M5. Run Layout And Release Chain

Goal: establish run-based outputs and release artifacts aligned with the PRD.

Delivered:

- `outputs/runs/<chapter>/<run_id>/...`
- `review/summary/teacher_summary.md`
- `release_manifest.yaml`
- `source_bundle/debug_index.md`

### M6. Teacher Change Loop

Goal: support propose-change, summarize-change, confirm-change, and scope-aware regeneration.

Delivered:

- `change_request.yaml`
- `change_summary.md`
- `change_confirmation.yaml`
- impact-scope regeneration logic

### M6.5 Hybrid Inference Cost-Control Lane

Goal: reduce cloud cost while keeping high-risk teaching reasoning on the cloud lane.

Remaining deliverables:

- successful `gemma4:e4b` pull completion inside the dedicated `Ubuntu-24.04` runtime
- smoke-test evidence for the local lane plus cloud fallback

### M7. WeCom End-to-End Integration

Goal: connect the official Hermes WeCom callback adapter to the course app.

Remaining deliverables:

- WeCom environment variables and callback config
- local callback setup instructions exercised against the live machine
- WeCom smoke-test evidence
- teacher interaction examples through the live channel

### M8. Regression And Local Operations

Goal: make the deployed system repeatable on the current machine.

Remaining deliverables:

- local startup command list
- logging and diagnosis notes
- end-to-end smoke-test writeup
- regression checklist and common-failure guidance

## Recommended Build Order

Proceed in this order:

1. `M1 Hermes Integration Skeleton`
2. `M2 Workflow Contract Refactor`
3. `M3 Toolization Of Existing Generators`
4. `M4 Course Agent And Subagent Setup`
5. `M5 Run Layout And Release Chain`
6. `M6 Teacher Change Loop`
7. `M6.5 Hybrid Inference Cost-Control Lane`
8. `M7 WeCom End-to-End Integration`
9. `M8 Regression And Local Operations`

## Immediate Next Slice

The immediate next slice is no longer `WSL2 official Hermes installation`.

That installation path is complete enough to move into hybrid routing implementation and then live integration.

Execute the next slice in this order:

1. retry `ollama pull gemma4:e4b` until the local model is fully available in `WSL2`
2. if the pull fails again, confirm the failure mode against `journalctl -u ollama -n 120 --no-pager` and the registry/blob `curl -Ivs` checks before assuming a new root cause
3. run `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor`
4. confirm that the fallback-log probe writes under `/root/.hermes-intellectual-tutor/logs/hybrid_router_fallback.jsonl`
5. then open `/root/.hermes-intellectual-tutor/.env` inside `WSL2`
6. provide the live cloud-model credentials needed for high-risk Hermes responses
7. provide `WECOM_CALLBACK_CORP_ID`, `WECOM_CALLBACK_CORP_SECRET`, `WECOM_CALLBACK_AGENT_ID`, `WECOM_CALLBACK_TOKEN`, and `WECOM_CALLBACK_ENCODING_AES_KEY`
8. optionally set `WECOM_CALLBACK_ALLOWED_USERS` for bring-up safety
9. start `hermes gateway run` or `hermes gateway start` with `HERMES_HOME=/root/.hermes-intellectual-tutor`
10. verify the callback endpoint can be reached and validated by WeCom
11. send the first allowed-user text message through WeCom and confirm Hermes receives and replies

Resume command bundle for the next session:

```bash
wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; systemctl is-active ollama; /usr/local/bin/ollama pull gemma4:e4b; /usr/local/bin/ollama list'
wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'journalctl -u ollama -n 120 --no-pager'
wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'getent ahosts registry.ollama.ai; timeout 20 curl -Ivs https://registry.ollama.ai/v2/ 2>&1 || true'
wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home "$HERMES_HOME"'
```

Only after this slice is verified should the plan advance to broader WeCom smoke coverage and local operations hardening.

## Anti-patterns

- rebuilding Hermes runtime inside this repository
- rebuilding a repo-local memory or summary system that duplicates official Hermes
- letting the WeCom callback call `generate_chapter.py` directly
- turning the course app into a new general-purpose agent platform
- collapsing notebook logic back into the top-level agent
- letting the local model become the primary teaching generator
- skipping `run_id`-based release governance before chat-loop testing
- maintaining two parallel runtimes for Hermes orchestration and repo-local orchestration
