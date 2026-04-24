# Repository Agent Guide

Use this file as the first-stop orientation doc for any future agent working in `D:\Codex_Project\intellectual_tutor`.

The goal is fast understanding, not full specification. For product decisions and execution status, always continue into the plan and PRD files listed below.

## Read Order

Read these files in this order before making non-trivial changes:

1. `AGENTS.md`
2. `plans/README.md`
3. `plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md`
4. `docs/PRD.md`
5. `README.md`

Use `docs/architecture/` and `docs/deployment/` only after the above context is loaded.

## Project Identity

This repository is a course-app layer that runs on top of the official `Hermes Agent`.

It is not:

- a replacement for Hermes core
- a standalone agent runtime
- a custom chat gateway
- a repo-local memory system

It is:

- a teacher-facing course-prep copilot
- a structured course-generation workflow
- a run-based artifact pipeline
- a WeCom-first Hermes application instance

The durable teaching thesis in this repo is:

`application problem -> mathematical abstraction -> model explanation -> experiment verification -> homework evaluation`

## Active Planning Source

Use these files as the only active planning sources:

- `plans/README.md`
- `plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md`
- `docs/PRD.md`

Do not recreate an alternative implementation plan only in chat.

## Progress Synchronization Rule

After every meaningful execution step, synchronize status back into the repository plan.

At minimum, update the active plan when any of the following changes:

- a milestone starts
- a milestone completes
- the next execution pointer changes
- a blocker is discovered
- a blocker is removed
- the recommended next step changes

## What Must Be Updated

After each task batch, update the active plan files with:

1. current milestone status
2. what has been completed
3. what remains
4. the exact next step
5. blockers or assumptions
6. commands or verification evidence needed for the next session

## Files That Must Stay In Sync

Always keep these aligned:

- `plans/README.md`
- `plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md`

When the default resume point changes, also update:

- `README.md`
- `docs/README.md`

## Fast Project Map

Think about the repository in layers:

### Layer 1: Product And Execution Truth

- `docs/PRD.md`
  product boundary, teacher workflow, release intent, pause/resume notes
- `plans/`
  execution truth, milestone state, blocker state, exact next step
- `README.md`
  high-level repo entry and expected workflow

### Layer 2: Hermes App Wiring

- `configs/hermes/`
  dedicated Hermes-instance templates such as `SOUL.template.md` and `inference_policy.template.yaml`
- `agents/course-app/`
  top-level course agent and subagent prompt definitions
- `skills/course/intellectual-tutor-course-workflow/`
  workflow skill and execution policy that Hermes loads

This layer defines how the official Hermes runtime should behave for this course app.

### Layer 3: Workflow Contracts

- `schemas/course/`
  structured contracts for `lesson_plan`, `ppt_script`, `quality_review`, `release_manifest`, change request/confirmation, and related artifacts
- `configs/course.yaml`
  course-level defaults
- `configs/chapters/`
  chapter-level configuration such as `gradient_descent.yaml`

This layer defines what good structured output looks like.

### Layer 4: Source Inputs

- `sources/chapters/<chapter>/`
  source material used to generate a chapter package
- `sources/chapters/gradient_descent/content.yaml`
  canonical example of a lesson-level source bundle in the current repo
- `profiles/`
  profile/config inputs used by the generation flow

This layer is the content input side.

### Layer 5: Execution And Tooling

- `tools/`
  Hermes-callable wrappers around the repo's generation and review capabilities
- `scripts/`
  local orchestration, bootstrap, smoke checks, status inspection, and compatibility helpers

Rule of thumb:

- edit `tools/` when changing what Hermes can call
- edit `scripts/` when changing local orchestration or compatibility paths
- keep both aligned when a workflow contract changes

### Layer 6: Run Outputs And Evidence

- `outputs/runs/<chapter>/<run_id>/`
  canonical run-based artifact layout
- `outputs_lecture/`, `outputs_visual/`, `outputs_status_check/`, `outputs_m3_check/`
  prior sample outputs and verification snapshots

This layer is where you inspect real generated behavior instead of guessing.

## Important Directories

- `agents/README.md`
  explains the agent tree and the course-app prompt layout
- `agent_briefs/`
  supporting architecture briefs for the agent system
- `docs/architecture/`
  architecture explanations such as course-app overview and script-to-tool mapping
- `docs/deployment/`
  WSL2, Hermes, Ollama, and WeCom setup guidance
- `skills/README.md`
  skill structure overview for this repo

## Key Entry Scripts

These are the fastest code entry points for understanding behavior:

- `scripts/generate_chapter.py`
  main run-generation entry for lesson plan, PPT script, notebook, review, and release artifacts
- `scripts/apply_confirmed_change.py`
  apply an approved change and regenerate only the impacted scope
- `scripts/read_run_status.py`
  inspect run state and summarize run outputs
- `scripts/bootstrap_hermes_course_app.py`
  materialize repo templates into a dedicated `HERMES_HOME`
- `scripts/check_hybrid_inference.py`
  smoke-check the local-vs-cloud routing setup for the Hermes instance

## Key Hermes Tools

These are the main tool wrappers that future agents should inspect before editing workflow behavior:

- `tools/lesson_plan_builder.py`
- `tools/ppt_designer.py`
- `tools/notebook_builder.py`
- `tools/verification.py`
- `tools/release_packager.py`
- `tools/status_reader.py`
- `tools/change_applier.py`

If behavior changes at the workflow level, inspect these before patching prompts.

## Best Concrete Example In This Repo

Use `gradient_descent` as the default reference chapter.

Start here:

- `configs/chapters/gradient_descent.yaml`
- `sources/chapters/gradient_descent/content.yaml`
- `sources/chapters/gradient_descent/ppt_script.yaml`
- `outputs/runs/gradient_descent/`

This is the best end-to-end example of how configs, sources, scripts, tools, schemas, and outputs fit together.

## Task To File Map

Use this quick routing table when deciding where to work:

- product scope, teacher workflow, or release boundary
  go to `docs/PRD.md`, `README.md`, and `docs/architecture/`
- Hermes persona, routing policy, or local/cloud split
  go to `configs/hermes/`, `agents/course-app/`, `skills/course/intellectual-tutor-course-workflow/`, and `scripts/bootstrap_hermes_course_app.py`
- output contract or schema drift
  go to `schemas/course/`, then align `tools/` and `scripts/`
- chapter generation logic
  go to `scripts/generate_chapter.py` plus the relevant files under `tools/`
- change-confirmation and scoped regeneration
  go to `scripts/apply_confirmed_change.py` and `tools/change_applier.py`
- run inspection or debugging
  go to `scripts/read_run_status.py` and the relevant path under `outputs/runs/`
- WeCom or Hermes deployment
  go to `docs/deployment/` and the active plan

## Resume Rule For New Sessions

If a new session starts with `continue the plan` or an equivalent Chinese resume request, read these files first and resume from the recorded execution pointer instead of re-deriving status from scratch:

1. `plans/README.md`
2. the active implementation plan
3. `docs/PRD.md`

## Current Default Resume Point

Unless the plan files are updated later, the current default resume point is:

1. enter `WSL2` distro `Ubuntu-24.04` as `root`
2. keep `HERMES_HOME=/root/.hermes-intellectual-tutor`
3. retry `ollama pull gemma4:e4b` until `ollama list` shows the model
4. run `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor`
5. only after that smoke check passes, continue to cloud-model credentials and WeCom callback validation

## Current Live Blocker

- `gemma4:e4b` pull attempts are currently timing out against `registry.ollama.ai`; do not advance to `.env` or WeCom callback work until the model is locally available

## Anti-Patterns To Avoid

- rebuilding Hermes core inside this repository
- creating a second repo-local memory or summary subsystem
- editing prompts while ignoring schema or tool contract drift
- treating `outputs/` as disposable when it contains the clearest runtime evidence
- moving into `.env` or WeCom callback work before the local hybrid smoke check passes
