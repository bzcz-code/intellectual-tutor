---
name: intellectual-tutor-course-workflow
description: Course-prep workflow for Intellectual Tutor on Hermes Agent. Use when handling teacher requests to generate a chapter package, summarize changes, or route re-generation safely.
version: 0.1.0
metadata:
  hermes:
    category: education
---

# Intellectual Tutor Course Workflow

## When to Use

Use this skill when the teacher asks to:

- generate a teaching package for a chapter
- query the status of a recent run
- propose changes to teaching content
- confirm a previously summarized change

## Procedure

1. Classify the request before choosing a model or tool:
   local-lane eligible or cloud-lane required.
2. Local lane is limited to:
   simple teacher questions, status explanations, fixed-format helper drafts, and candidate run summaries.
3. Cloud lane is required for:
   `Professor Architect Agent` orchestration, lesson-plan generation, core subagent generation, `quality_review`, source governance, and release gating.
4. If the request is ambiguous about chapter scope, ask a clarification question before routing work.
5. If the request is not clearly local-lane eligible, route it to the cloud lane directly.
6. If a local call fails or is uncertain, log the miss and upgrade to the cloud lane.
7. For write requests, produce a natural-language change summary before any file-changing tool is called.
8. Only after explicit confirmation, route work to the appropriate course tool chain.
9. Keep the course-level baseline and governance rules unchanged unless the user is operating through an approved config workflow.

## Current Boundaries

- This skill defines workflow behavior, not final file rendering.
- Final PPTX, DOCX, and IPYNB generation belongs to course tools.
- This skill should work with the dedicated Intellectual Tutor Hermes instance, not a generic assistant identity.

## Verification

A correct run should preserve these properties:

- no silent chapter guessing
- no silent downgrade of cloud-only teaching work onto the local lane
- local misses leave a trace before cloud upgrade
- no direct write execution before confirmation
- no tool invents teaching content beyond approved structured inputs
