# Script To Tool Mapping

## Purpose

This document maps the current local generator scripts to the future Hermes course app tool surface.

The current scripts are useful implementation assets, but they are not yet the final Hermes integration API.

## Mapping Table

| Current file | Current role | Future role |
| --- | --- | --- |
| `scripts/generate_chapter.py` | Local orchestration entry | Debug wrapper only, or thin local compatibility entry |
| `scripts/lesson_planner.py` | Lesson planning + DOCX + notebook generation | Split into `lesson_plan_builder` and `notebook_builder` |
| `scripts/ppt_subagent.py` | Slide script validation | Validation helper for `PPT Script Subagent` contract |
| `scripts/ppt_skill.py` | PPT rendering and PPT report | `ppt_designer` tool |
| `scripts/verify_outputs.py` | Artifact verification | `verification` tool |

## Required Refactors

### 1. Remove Mixed Responsibilities

`lesson_planner.py` currently mixes:

- lesson planning
- DOCX generation
- notebook generation
- quality report writing

Future state:

- lesson planning logic stays near course orchestration
- file generation moves into tools
- notebook generation becomes its own execution path

### 2. Replace Script-Centric Entry Points

Current entry points are shaped around local CLI use.

Future tools must accept stable structured inputs such as:

- lesson plan path
- chapter config path
- output root
- run id

### 3. Preserve Existing Implementation Value

The refactor should reuse current code where possible.

The goal is not a rewrite-from-scratch; the goal is to expose these capabilities as Hermes-friendly tools with clear contracts.
