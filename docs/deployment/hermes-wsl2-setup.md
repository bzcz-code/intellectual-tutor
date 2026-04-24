# Hermes WSL2 Setup

## Purpose

This document defines the supported way to run `Intellectual Tutor` on the current Windows machine:

- Windows hosts the repo and local files.
- `WSL2` runs the official `Hermes Agent`.
- Hermes loads this repository as a course app via external skills and project context files.

This repo does not vendor Hermes itself.

## Supported Topology

Windows workspace:

```text
D:\Codex_Project\intellectual_tutor
```

WSL2 mount path:

```text
/mnt/d/Codex_Project/intellectual_tutor
```

Hermes home:

```text
~/.hermes
```

Recommended custom instance home for this project:

```text
~/.hermes-intellectual-tutor
```

Use a dedicated `HERMES_HOME` so this course app runs as a clean, course-specific Hermes instance.

## Preconditions

Before using this guide, the following must already be true:

- WSL2 is installed and working.
- Python 3.11 is available in WSL2.
- The Windows repo path is readable from WSL2.
- You have a model provider plan ready for Hermes.
- For the approved hybrid path, this means native Windows `Ollama` for low-risk requests plus a live cloud provider for high-risk teaching tasks.

## Install Hermes In WSL2

Follow the official Hermes install path inside WSL2.

Reference:

- Hermes README install commands
- Hermes docs quickstart

At the time of writing, the official contributor/dev path is:

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
./setup-hermes.sh
```

Or the manual path:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all,dev]"
```

## Create A Dedicated Hermes Home

Inside WSL2:

```bash
mkdir -p ~/.hermes-intellectual-tutor
export HERMES_HOME=~/.hermes-intellectual-tutor
```

This instance-specific home will contain:

```text
$HERMES_HOME/
├── config.yaml
├── .env
├── SOUL.md
├── memories/
└── skills/
```

## Connect This Repo As A Course App

This repo should be mounted into Hermes using two mechanisms:

1. Project context files from the workspace itself
2. External skill directories declared in Hermes `config.yaml`

Recommended `config.yaml` fragment:

```yaml
skills:
  external_dirs:
    - /mnt/d/Codex_Project/intellectual_tutor/skills
```

Why this layout:

- Hermes keeps its writable local skills in `~/.hermes/skills/`
- This repo stays source-controlled and read-only from Hermes's perspective
- The course app can evolve without copying files into Hermes every time

## Windows-hosted Ollama For WSL2 Hermes

For the approved cost-control path, run `Ollama` natively on Windows and let the dedicated Hermes instance in `WSL2` call it through `OLLAMA_BASE_URL`.

Install it on Windows with the official Windows installer, then pull the local model on Windows:

```powershell
ollama pull gemma4:26b
```

If the machine uses a local HTTP proxy instead of a full-device `TUN` or global tunnel, make sure the Windows `Ollama` process actually inherits `HTTP_PROXY` and `HTTPS_PROXY` before retrying a large pull. On this machine the system proxy may be enabled while `Ollama` still starts with blank proxy environment variables, which leads to repeated partial downloads without registering the model.

Recommended baseline:

- `Ollama` listens on port `11434` on the Windows host
- Hermes reaches it from `WSL2` through `OLLAMA_BASE_URL`
- the default local model for this project is `gemma4:26b`

Why this topology:

- it avoids the current machine behavior where `WSL2` is reclaimed even while background `systemd` services still exist
- the long model pull no longer depends on keeping the distro alive through a foreground client session
- fallback from local to cloud stays a provider decision, not a `WSL2` lifecycle decision

The local lane is for:

- simple teacher questions
- run-status and artifact explanations
- fixed-format helper drafts
- candidate summaries that may later be curated into Hermes memory

The local lane is not for:

- core `Professor Architect Agent` decisions
- first-pass lesson planning
- quality gates, source governance, or release decisions

## SOUL Strategy

Hermes loads `SOUL.md` only from `HERMES_HOME`, not from the current repo.

For this project:

- Keep the active instance SOUL in `$HERMES_HOME/SOUL.md`
- Keep a tracked template in this repo under `configs/hermes/SOUL.template.md`

The repo template is the source of truth for versioned review.
The Hermes home copy is the live instance file.

## Recommended Startup Sequence

Inside WSL2:

```bash
export HERMES_HOME=~/.hermes-intellectual-tutor
cd /path/to/hermes-agent
hermes gateway start
```

Before gateway bring-up, set `OLLAMA_BASE_URL` in `$HERMES_HOME/.env` to the Windows-hosted endpoint that is reachable from `WSL2`.

Try `127.0.0.1` first. If that does not work from `WSL2`, use the Windows host address exposed to the distro, which on this machine can be discovered from `/etc/resolv.conf`.

Example endpoint discovery inside `WSL2`:

```bash
WINDOWS_HOST="$(awk '/nameserver/ {print $2; exit}' /etc/resolv.conf)"
echo "$WINDOWS_HOST"
```

Then verify the Windows-hosted `Ollama` endpoint from `WSL2`:

```bash
curl http://127.0.0.1:11434/api/chat -d '{
  "model": "gemma4:26b",
  "messages": [{"role": "user", "content": "ping"}],
  "stream": false
}' || curl "http://$WINDOWS_HOST:11434/api/chat" -d '{
  "model": "gemma4:26b",
  "messages": [{"role": "user", "content": "ping"}],
  "stream": false
}'
```

If `curl` from `WSL2` reaches the endpoint but `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py` still fails with `404 Not Found`, the Windows `Ollama` server is reachable and the remaining issue is that `gemma4:26b` is not installed locally yet.

Then run the repo-side hybrid-lane smoke check:

```bash
export HERMES_HOME=~/.hermes-intellectual-tutor
python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home "$HERMES_HOME"
```

Or for CLI-only testing:

```bash
export HERMES_HOME=~/.hermes-intellectual-tutor
cd /mnt/d/Codex_Project/intellectual_tutor
hermes
```

## Verification Checklist

- `echo $HERMES_HOME` points to the dedicated course instance
- `test -f $HERMES_HOME/SOUL.md` succeeds
- `hermes skills list` can see repo-provided skills after `external_dirs` is configured
- Hermes launched from WSL2 can access `/mnt/d/Codex_Project/intellectual_tutor`
- Repo `AGENTS.md` and project files are discoverable from the active workspace
- if local inference is enabled, the configured `OLLAMA_BASE_URL` reaches the Windows-hosted `Ollama` endpoint from `WSL2`
- `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py` succeeds and writes a fallback-log probe under `$HERMES_HOME/logs/`

## Notes

- Do not run the production course instance from default `~/.hermes` if that home is also used for unrelated agents.
- Do not copy the repo `skills/` tree into `~/.hermes/skills/` by hand unless debugging. Prefer `skills.external_dirs`.
- Do not store Feishu secrets in this repo. They belong in `$HERMES_HOME/.env`.
- Do not replace official Hermes memory, `memory` tool, or `session_search` with a repo-local summary clone. The course app may only add routing policy on top.
