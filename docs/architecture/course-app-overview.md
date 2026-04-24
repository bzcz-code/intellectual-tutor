# Course App Overview

## Role Of This Repository

`D:\Codex_Project\intellectual_tutor` is not the Hermes core repository.

Its role is:

- a Hermes course app
- a course workflow repository
- a deployment and integration guide for the course-specific Hermes instance

## System Model

### Layer 1. Official Hermes Core

External runtime running in WSL2:

- SOUL loading
- memory
- summary / cleanup
- messaging gateway
- platform adapters
- subagent orchestration
- skill loading
- tool calling

### Layer 2. Course App

This repo defines the course-specific behavior:

- course identity and prompts
- workflow contracts
- source governance
- quality gates
- release and summary artifacts
- WeCom interaction policy

### Layer 3. Course Execution Assets

Concrete course outputs and generators:

- lesson plan
- PPT script
- notebook script
- PPT / DOCX / IPYNB generation
- verification
- packaging

## Hermes Loading Model

This repo integrates with Hermes in three ways:

1. `SOUL.template.md`
   - versioned template stored in this repo
   - copied into `$HERMES_HOME/SOUL.md`

2. repo `skills/`
   - scanned by Hermes through `skills.external_dirs`
   - provides course workflow knowledge

3. workspace context files
   - repo `AGENTS.md`
   - PRD and architecture docs
   - source/config files the tools operate on

## Repo-Level Integration Layout

Planned integration layout in this repo:

```text
configs/hermes/
  SOUL.template.md
  config.template.yaml
  env.template

agents/course-app/
  ProfessorArchitectAgent.md
  PPTScriptSubagent.md
  NotebookLabSubagent.md
  QualityReviewSubagent.md
  SourceCuratorSubagent.md

skills/course/
  intellectual-tutor-course-workflow/
    SKILL.md

tools/
  ... future course tools ...
```

## Why SOUL And Agent Prompts Are Split

`SOUL.md` is instance identity and must live in `HERMES_HOME`.

This repo should only track a template because:

- the live SOUL belongs to the Hermes instance
- the repo should version the intended identity
- the deployed instance may contain local secrets or operator-specific edits

Agent prompts remain in the repo because they are course-app logic, not Hermes core identity.

## Current Generator Mapping

Current scripts are implementation assets, not final Hermes integration points.

Mapping:

- `scripts/lesson_planner.py`
  - future: `tools/lesson_plan_builder.py`
- `scripts/ppt_subagent.py`
  - future: subagent contract validation + `PPT Script Subagent` support
- `scripts/ppt_skill.py`
  - future: `tools/ppt_designer.py`
- `scripts/verify_outputs.py`
  - future: `tools/verification.py`
- `scripts/generate_chapter.py`
  - future: compatibility wrapper or local debug entry only

## M1 Exit Condition

M1 is complete when:

- the repo has a documented Hermes mounting model
- a dedicated SOUL template exists
- the agent/subagent prompt skeleton exists
- a valid external skill skeleton exists
- future tool boundaries are mapped from current scripts
