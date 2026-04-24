# Plans Index

Use this file as the plan entry point for new sessions.

## Active Plan

- [2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md](2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md)

## Plan Status

This is the only current implementation plan in the repository.

It supersedes the earlier wrong route that treated this repository as a self-built Hermes runtime.

## Current Execution Pointer

If a new session starts with "继续完成计划" or "continue the plan", the next execution step is not repo-internal scaffolding.

The next step is:

1. enter `WSL2`
2. install the official `Hermes Agent`
3. create the dedicated `HERMES_HOME`
4. mount this repository as the course app
5. then proceed to WeCom callback integration and end-to-end smoke testing

Use these documents in that order:

- [../docs/deployment/hermes-wsl2-setup.md](../docs/deployment/hermes-wsl2-setup.md)
- [../docs/deployment/wecom-setup.md](../docs/deployment/wecom-setup.md)
- [2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md](2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md)

## Progress Sync Rule

After every meaningful execution step, the active plan must be updated before the session ends.

The plan update must record:

- current milestone status
- completed work
- remaining work
- exact next step
- blockers or assumptions
- verification evidence when relevant

This rule exists so a future session can resume from the plan files without reconstructing progress from chat history.

## Rule For New Sessions

When a new session asks for implementation order, milestones, or next steps:

- use the active plan above
- treat repo-side scaffolding milestones as already completed unless evidence shows otherwise
- start execution from WSL2 Hermes installation
- trust the latest progress recorded in the plan files
- do not recreate or reference the removed self-built-Hermes plan
