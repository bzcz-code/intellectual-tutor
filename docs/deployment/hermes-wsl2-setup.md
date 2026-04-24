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
- For the approved hybrid path, this means local `Ollama` in `WSL2` for low-risk requests plus a live cloud provider for high-risk teaching tasks.

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

## Local Ollama Sidecar In WSL2

For the approved cost-control path, run `Ollama` in the same `WSL2` environment as Hermes.

Install it inside the distro with the official Linux installer:

```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable ollama
sudo systemctl start ollama
ollama pull gemma4
```

Recommended baseline:

- `Ollama` listens on `127.0.0.1:11434`
- Hermes reaches it through the local loopback address, not through a Windows-host bridge
- the default local model for this project is `gemma4`

Why this topology:

- no Windows-to-WSL network indirection is required
- local helper calls and simple-question routing can use a single stable endpoint
- fallback from local to cloud stays a provider decision, not a networking decision

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

If the local sidecar is enabled, validate it before gateway bring-up:

```bash
curl http://127.0.0.1:11434/api/chat -d '{
  "model": "gemma4",
  "messages": [{"role": "user", "content": "ping"}],
  "stream": false
}'
```

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
- if local inference is enabled, `curl http://127.0.0.1:11434/api/chat` succeeds from the same distro
- `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py` succeeds and writes a fallback-log probe under `$HERMES_HOME/logs/`

## Notes

- Do not run the production course instance from default `~/.hermes` if that home is also used for unrelated agents.
- Do not copy the repo `skills/` tree into `~/.hermes/skills/` by hand unless debugging. Prefer `skills.external_dirs`.
- Do not store WeCom secrets in this repo. They belong in `$HERMES_HOME/.env`.
- Do not replace official Hermes memory, `memory` tool, or `session_search` with a repo-local summary clone. The course app may only add routing policy on top.
