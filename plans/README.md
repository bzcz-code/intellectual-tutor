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

1. enter `WSL2` distro `Ubuntu-24.04` as `root`
2. keep `HERMES_HOME=/root/.hermes-intellectual-tutor`
3. retry `ollama pull gemma4:e4b` from that dedicated runtime until the model appears in `ollama list`
4. once `gemma4:e4b` is present, run:
   `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor`
5. only after the hybrid smoke check passes, continue to cloud credentials and WeCom callback validation

The next step is:

1. finish the local-model bring-up by completing `ollama pull gemma4:e4b` inside `WSL2`
2. run the repo-side hybrid smoke check:
   `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor`
3. confirm fallback-log writing under `/root/.hermes-intellectual-tutor/logs/hybrid_router_fallback.jsonl`
4. keep official Hermes memory, `memory` tool, and `session_search` as the only built-in memory/summary path
5. keep a live cloud provider for:
   `Professor Architect Agent`, core subagent generation, `quality_review`, source governance, and release gating
6. then continue with live cloud-model and WeCom callback credentials in `$HERMES_HOME/.env`
7. resume WeCom callback validation and end-to-end smoke testing

Current live blocker:

- `gemma4:e4b` pull attempts now reach both `registry.ollama.ai` and the signed Cloudflare blob host, but the large blob download still fails with `EOF`, `unexpected EOF`, and intermittent `dial tcp 198.18.0.201/202:443: i/o timeout`; `ollama list` is still empty and partial blob files remain under `/usr/share/ollama/.ollama/models/blobs/`

Use these documents in that order:

- [../AGENTS.md](../AGENTS.md)
- [../docs/PRD.md](../docs/PRD.md)
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
- treat WSL2, official Hermes installation, dedicated `HERMES_HOME`, and repo skill mounting as already completed unless evidence shows otherwise
- treat the current design decision as:
  `Ollama` in `WSL2` for low-risk requests, official Hermes memory for summaries, cloud provider for high-risk teaching work
- resume from hybrid routing implementation before broad WeCom rollout unless evidence shows it is already complete
- trust the latest progress recorded in the plan files
- do not recreate or reference the removed self-built-Hermes plan
