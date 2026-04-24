# Intellectual Tutor: A Hermes Course App

This repository is not the Hermes core.

It is a university teaching copilot that runs on top of the official Hermes Agent.

Its final product goal is to help teachers in the AI math foundation course cluster generate complete chapter teaching packages through WeCom, revise them through dialogue, accumulate confirmed teaching preferences, and keep course context across later chapters instead of acting as only a one-off single-chapter generator.

## Active Entry Points

Start here in any new session:

- Active product definition: [docs/PRD.md](docs/PRD.md)
- Active implementation plan: [plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md](plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md)
- Docs index: [docs/README.md](docs/README.md)
- Plans index: [plans/README.md](plans/README.md)

These are the only current planning documents.

## Repository Role

This repo provides:

- course-app prompts, skills, tools, and workflow contracts
- deployment guidance for running the course app with official Hermes in WSL2
- WeCom integration guidance for the course-specific Hermes instance
- hybrid local/cloud inference guidance for cost-aware routing

This repo does not provide:

- a self-built Hermes runtime
- a self-built memory system
- a self-built messaging gateway

## Current Architecture

The active system boundary is:

`Official Hermes Core -> Intellectual Tutor Course App -> Course Tools / Artifacts`

The approved inference split is:

- official Hermes memory, `memory` tool, and `session_search` remain the built-in summary and recall path
- local `Ollama + gemma4` in `WSL2` handles low-risk questions and helper drafts
- a live cloud provider remains required for high-risk teaching generation and review

Inside this repo, the course layer is organized as:

- `agents/`
  course-specific main-agent and subagent prompt templates
- `skills/`
  repo-tracked external Hermes skills
- `tools/`
  executable course tools backed by the current generator pipeline
- `schemas/course/`
  workflow contracts for lesson plan, ppt script, notebook script, review, release, and teacher change flow
- `docs/deployment/`
  WSL2 and WeCom setup guides

## Current Status

The repo-side course runtime is already in place:

- run-based output layout under `outputs/runs/<chapter>/<run_id>/...`
- structured lesson-plan contract plus legacy compatibility bridge
- teacher change summary and explicit confirmation flow
- partial regeneration of DOCX, notebook, review, and PPT after confirmed changes

Already completed on the current machine:

- `WSL2` distro `Ubuntu-24.04`
- official Hermes install under `/root/.hermes-intellectual-tutor/hermes-agent`
- dedicated `HERMES_HOME=/root/.hermes-intellectual-tutor`
- repo skill mounting via `/mnt/d/Codex_Project/intellectual_tutor/skills`

What is still external:

- completing the local `gemma4:e4b` bring-up and hybrid smoke check
- populating the dedicated Hermes instance with live model-provider credentials
- populating the dedicated Hermes instance with live WeCom callback secrets
- starting and validating the Hermes gateway callback path
- connecting the official WeCom callback adapter
- running the first real Hermes -> WeCom end-to-end smoke test

Current blocker:

- the repo-side hybrid-routing implementation is in place, but the live resume point is still blocked on `ollama pull gemma4:e4b` timing out against `registry.ollama.ai` before the local-lane smoke check can run

Current default resume point:

- enter `Ubuntu-24.04` as `root`
- keep `HERMES_HOME=/root/.hermes-intellectual-tutor`
- finish `ollama pull gemma4:e4b`
- run `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor`
- only then continue to `.env` credential wiring and WeCom callback validation

If a new session says "continue the plan" or "继续完成计划", start from hybrid routing implementation on top of the existing WSL2 Hermes install rather than from repo-internal scaffolding.

## Historical Note

`docs/MVP.md` is retained only as a historical note for the earlier local single-chapter pipeline.

Do not use `docs/MVP.md` as the active product definition or implementation plan.
