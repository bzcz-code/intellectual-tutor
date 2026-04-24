# Intellectual Tutor: A Hermes Course App

This repository is not the Hermes core.

It is a university teaching copilot that runs on top of the official Hermes Agent.

Its final product goal is to help teachers in the AI math foundation course cluster generate complete chapter teaching packages through Feishu, revise them through dialogue, accumulate confirmed teaching preferences, and keep course context across later chapters instead of acting as only a one-off single-chapter generator.

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
- deployment guidance for connecting that WSL2 Hermes instance to native Windows `Ollama`
- Feishu integration guidance for the course-specific Hermes instance
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
- native Windows `Ollama + gemma4:26b` handles low-risk questions and helper drafts for the Hermes instance running in `WSL2`
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
  WSL2 and Feishu setup guides

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

- populating the dedicated Hermes instance with live model-provider credentials
- populating the dedicated Hermes instance with live Feishu credentials
- starting and validating the Hermes gateway Feishu path
- connecting the official Hermes Feishu/Lark adapter
- running the first real Hermes -> Feishu end-to-end smoke test

Current blocker:

- the active blocker is now the local-model switch to `gemma4:26b`: Windows `Ollama 0.21.1` is installed, `WSL2` can reach the Windows-hosted endpoint, but `gemma4:26b` is not yet available locally and the current Windows `Ollama` service appears to start without `HTTP_PROXY` or `HTTPS_PROXY` even though the machine proxy is enabled

Current default resume point:

- verify native Windows `Ollama 0.21.1` is still installed and serving `http://127.0.0.1:11434`
- make the Windows `Ollama` process inherit the required proxy path or confirm the proxy is `TUN` / global enough for large blob downloads
- complete `ollama pull gemma4:26b` on Windows
- enter `Ubuntu-24.04` as `root`
- keep `HERMES_HOME=/root/.hermes-intellectual-tutor`
- confirm `OLLAMA_BASE_URL=http://172.29.0.1:11434` is still present in `/root/.hermes-intellectual-tutor/.env`
- confirm `LOCAL_FAST_MODEL=gemma4:26b` is still present in `/root/.hermes-intellectual-tutor/.env`
- rerun `scripts/check_hybrid_inference.py`
- only then continue to `.env` credential wiring and Feishu validation

If a new session says "continue the plan" or "继续完成计划", start from hybrid routing implementation on top of the existing WSL2 Hermes install rather than from repo-internal scaffolding.

## Historical Note

`docs/MVP.md` is retained only as a historical note for the earlier local single-chapter pipeline.

Do not use `docs/MVP.md` as the active product definition or implementation plan.
