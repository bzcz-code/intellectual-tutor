# Docs Index

Use this file as the documentation entry point for new sessions.

## Active Documents

- Product definition: [PRD.md](PRD.md)
- Architecture overview: [architecture/course-app-overview.md](architecture/course-app-overview.md)
- Script-to-tool mapping: [architecture/script-to-tool-mapping.md](architecture/script-to-tool-mapping.md)
- WSL2 deployment: [deployment/hermes-wsl2-setup.md](deployment/hermes-wsl2-setup.md)
- WeCom deployment: [deployment/wecom-setup.md](deployment/wecom-setup.md)

## Historical Documents

- Historical local chapter-pipeline note: [MVP.md](MVP.md)

## Rule For New Sessions

For current planning and implementation decisions:

- use `docs/PRD.md`
- use the active plan in `plans/`
- treat WSL2 Hermes installation as completed unless the machine has been reset
- treat the approved runtime split as:
  `Ollama` in `WSL2` for low-risk requests, official Hermes memory for summaries, cloud provider for high-risk teaching work
- treat the current restore point as:
  finish `ollama pull gemma4:e4b` in `/root/.hermes-intellectual-tutor`, then run `scripts/check_hybrid_inference.py`, then continue to `.env` and WeCom bring-up
- resume from hybrid routing implementation before broad WeCom rollout unless evidence shows it is already complete
- do not treat `docs/MVP.md` as the current spec
