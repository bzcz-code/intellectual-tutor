# Repository Work Rules

These rules apply to all future work in this repository.

## Active Planning Source

Use these files as the only active planning sources:

- `plans/README.md`
- `plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md`
- `docs/PRD.md`

Do not recreate an alternative plan in chat without updating the repository plan files.

## Progress Synchronization Rule

After every meaningful execution step, the agent must synchronize progress back into the repository plan.

This is mandatory.

At minimum, update the active plan when any of the following happens:

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
5. any blockers or assumptions
6. any commands or verification evidence that the next session needs

## Required Files To Keep In Sync

The following files must stay aligned:

- `plans/README.md`
- `plans/2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md`

When the default resume point changes, also update:

- `README.md`
- `docs/README.md`

## Resume Rule For New Sessions

A new session that starts with requests like:

- "继续完成计划"
- "continue the plan"
- "继续"

must first read:

1. `plans/README.md`
2. the active implementation plan
3. `docs/PRD.md`

and then continue from the recorded execution pointer instead of re-deriving status from scratch.

## Current Default Resume Point

Unless the plan files are updated later, the current default resume point is:

1. enter `WSL2`
2. install the official `Hermes Agent`
3. create the dedicated `HERMES_HOME`
4. mount this repository as the course app
5. continue to WeCom callback integration and smoke testing
