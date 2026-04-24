# Intellectual Tutor: A Hermes Course App

This repository is not the Hermes core.

It is a course-prep app that runs on top of the official Hermes Agent and is currently scoped to university AI teaching workflows.

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

This repo does not provide:

- a self-built Hermes runtime
- a self-built memory system
- a self-built messaging gateway

## Current Architecture

The active system boundary is:

`Official Hermes Core -> Intellectual Tutor Course App -> Course Tools / Artifacts`

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

What is still external:

- installing official Hermes in WSL2
- wiring the live `HERMES_HOME`
- connecting the official WeCom callback adapter
- running the first real Hermes -> WeCom end-to-end smoke test

## Historical Note

`docs/MVP.md` is retained only as a historical note for the earlier local single-chapter pipeline.

Do not use `docs/MVP.md` as the active product definition or implementation plan.
