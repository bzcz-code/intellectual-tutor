# Plans Index

Use this file as the plan entry point for new sessions.

## Active Plan

- [2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md](2026-04-24-intellectual-tutor-hermes-course-app-implementation-plan.md)

## Plan Status

This is the only current implementation plan in the repository.

It supersedes the earlier wrong route that treated this repository as a self-built Hermes runtime.

## Current Execution Pointer

If a new session starts with "continue the plan" or "继续完成计划", do not restart repo scaffolding or WSL2/Hermes installation.

Current default resume point:

1. verify native Windows `Ollama 0.21.1` is still installed and serving `http://127.0.0.1:11434`
2. make the Windows `Ollama` process inherit the required proxy path or confirm the proxy is `TUN` / global enough for large blob downloads
3. complete `ollama pull gemma4:26b` on Windows
4. enter `WSL2` distro `Ubuntu-24.04` as `root`
5. keep `HERMES_HOME=/root/.hermes-intellectual-tutor`
6. confirm `/root/.hermes-intellectual-tutor/.env` still contains:
   `OLLAMA_BASE_URL=http://172.29.0.1:11434`
7. confirm `LOCAL_FAST_MODEL=gemma4:26b`
8. rerun `scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor`
9. continue with live cloud credentials in `$HERMES_HOME/.env`
10. continue with Feishu credentials and gateway validation

The next step is:

1. keep native Windows `Ollama 0.21.1` running and make sure the Windows `Ollama` process inherits the required proxy path or that the proxy is `TUN` / global enough for large blob downloads
2. complete `ollama pull gemma4:26b` on Windows
3. keep official Hermes memory, `memory` tool, and `session_search` as the only built-in memory/summary path
4. keep a live cloud provider for:
   `Professor Architect Agent`, core subagent generation, `quality_review`, source governance, and release gating
5. keep `OLLAMA_BASE_URL=http://172.29.0.1:11434` and `LOCAL_FAST_MODEL=gemma4:26b` in the dedicated Hermes instance
6. rerun `scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor`
7. continue with live cloud-model credentials in `$HERMES_HOME/.env`
8. continue with `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, and optional `FEISHU_ALLOWED_USERS`
9. start `hermes gateway run` or `hermes gateway start`
10. verify Feishu authentication and the first end-to-end smoke test

Current live blocker:

- the active blocker is the local-model switch to `gemma4:26b`: Windows `Ollama 0.21.1` is installed, `WSL2` reaches `http://172.29.0.1:11434`, and the dedicated Hermes instance is already configured for `gemma4:26b`, but `ollama list` is still empty so the local lane cannot yet be re-validated
- current evidence points to a Windows proxy mismatch: the machine proxy is enabled at `127.0.0.1:7897`, but the current `Ollama` service starts with blank `HTTP_PROXY` and `HTTPS_PROXY`

Use these documents in that order:

- [../AGENTS.md](../AGENTS.md)
- [../docs/PRD.md](../docs/PRD.md)
- [../docs/deployment/hermes-wsl2-setup.md](../docs/deployment/hermes-wsl2-setup.md)
- [../docs/deployment/feishu-setup.md](../docs/deployment/feishu-setup.md)
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
- treat WSL2, official Hermes installation, dedicated `HERMES_HOME`, and repo skill mounting as already completed unless evidence shows otherwise
- treat the current design decision as:
  native Windows `Ollama` for low-risk requests, official Hermes memory for summaries, and a cloud provider for high-risk teaching work
- resume from hybrid routing implementation before broad Feishu rollout unless evidence shows it is already complete
- trust the latest progress recorded in the plan files
- do not recreate or reference the removed self-built-Hermes plan

## Post-M7 Resume Rule

This rule activates only after the active implementation plan records all of the following:

- live cloud-provider credentials are validated for the dedicated Hermes instance
- the official Hermes Feishu/Lark adapter authenticates successfully
- the first end-to-end smoke test passes
- the verification evidence is written back into the active implementation plan

Once those conditions are recorded and no regression evidence exists:

- do not resume from hybrid inference bring-up
- do not resume from Feishu adapter bring-up
- do not reopen deployment tasks unless new evidence shows regression

Resume instead from:

- `docs/review/checklist_backlog.md`
- `P0` intake only

Promotion rule:

- move an item into `docs/PRD.md` only if it changes product boundary, acceptance criteria, or operating rules
- move an item into the active implementation plan only if it is approved as near-term execution work
- keep all other review items in `docs/review/` until explicitly promoted

The first post-M7 execution slice is:

1. intake `P0` items from `docs/review/checklist_backlog.md`
2. select the smallest set that improves reliability or acceptance quality without widening scope
3. sync accepted items into the active planning sources before implementation
