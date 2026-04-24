# Docs Index

Use this file as the documentation entry point for new sessions.

## Active Documents

- Product definition: [PRD.md](PRD.md)
- Architecture overview: [architecture/course-app-overview.md](architecture/course-app-overview.md)
- Script-to-tool mapping: [architecture/script-to-tool-mapping.md](architecture/script-to-tool-mapping.md)
- WSL2 deployment: [deployment/hermes-wsl2-setup.md](deployment/hermes-wsl2-setup.md)
- Feishu deployment: [deployment/feishu-setup.md](deployment/feishu-setup.md)

## Historical Documents

- Historical local chapter-pipeline note: [MVP.md](MVP.md)

## Rule For New Sessions

For current planning and implementation decisions:

- use `docs/PRD.md`
- use the active plan in `plans/`
- treat WSL2 Hermes installation as completed unless the machine has been reset
- treat the approved runtime split as:
  native Windows `Ollama` for low-risk requests, official Hermes memory for summaries, and a cloud provider for high-risk teaching work
- treat the current restore point as:
  verify native Windows `Ollama`, make sure the Windows `Ollama` process inherits the required proxy path or the proxy is `TUN` / global enough for `gemma4:26b`, confirm `OLLAMA_BASE_URL=http://172.29.0.1:11434` plus `LOCAL_FAST_MODEL=gemma4:26b` are still set in `/root/.hermes-intellectual-tutor/.env`, then continue to cloud credentials and Feishu bring-up
- resume from hybrid routing implementation before broad Feishu rollout unless evidence shows it is already complete
- do not treat `docs/MVP.md` as the current spec
