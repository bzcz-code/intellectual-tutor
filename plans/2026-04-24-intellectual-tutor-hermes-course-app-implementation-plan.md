# Intellectual Tutor Hermes Course App Implementation Plan

## Objective

Upgrade `D:\Codex_Project\intellectual_tutor` from a local single-chapter generation repository into:

- a course-prep app that runs on top of the official `Hermes Agent`
- a course instance that uses the official `Feishu / Lark` adapter as the teacher entry point
- a v1 teacher loop covering generate package, query status, propose change, explicit confirmation, and regeneration

This plan explicitly rejects the earlier wrong route of building a separate Hermes runtime, memory system, or messaging gateway inside this repository.

## Current Execution Pointer

The repository-side course-app scaffolding is already in place.

When continuing this plan, do not restart from early repo-internal scaffolding tasks or from initial WSL2/Hermes installation unless the machine has been reset.

The next execution slice is:

1. implement the approved hybrid local/cloud inference policy in docs, templates, and runtime wiring
2. install and validate native Windows `Ollama` for the dedicated Hermes instance running in `WSL2`
3. use `gemma4:26b` as the local low-cost lane for:
   simple questions, status explanations, fixed-format helper drafts, and candidate run summaries
4. keep official Hermes memory, `memory` tool, and `session_search` as the only built-in memory/summary path
5. keep a live cloud provider for:
   `Professor Architect Agent`, core subagent generation, `quality_review`, source governance, and release gating
6. auto-upgrade local failures or uncertainty to the cloud lane and log the local miss
7. after the hybrid lane is validated, continue with live cloud credentials and Feishu secrets in `$HERMES_HOME/.env`
8. resume Feishu authentication and the end-to-end smoke test

Current default resume point:

1. install or verify native Windows `Ollama`
2. pull `gemma4:26b` on Windows
3. open `Ubuntu-24.04` in `WSL2` as `root`
4. export `HERMES_HOME=/root/.hermes-intellectual-tutor`
5. set `OLLAMA_BASE_URL` in `/root/.hermes-intellectual-tutor/.env` to the Windows-hosted endpoint reachable from `WSL2`
6. run the repo-side smoke check:
   `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor`
7. if that passes, move directly into `$HERMES_HOME/.env` cloud-provider and Feishu secret configuration

Primary references:

- `docs/PRD.md`
- `docs/deployment/hermes-wsl2-setup.md`
- `docs/deployment/feishu-setup.md`
- `scripts/bootstrap_hermes_course_app.py`

Rule for new sessions:

- If the user says "continue the plan" or "继续完成计划", start from hybrid routing implementation on top of the existing WSL2 Hermes install.
- Do not restart from M1 document scaffolding unless files are missing.

## Execution Update 2026-04-24

Completed in prior execution:

- installed `WSL2` distro `Ubuntu-24.04`
- verified `WSL2` entry with `root`, kernel visibility, and repo mount at `/mnt/d/Codex_Project/intellectual_tutor`
- installed the official `Hermes Agent` into `/root/.hermes-intellectual-tutor/hermes-agent`
- initialized dedicated `HERMES_HOME=/root/.hermes-intellectual-tutor`
- ran `scripts/bootstrap_hermes_course_app.py` inside `WSL2`
- verified `config.yaml` contains `skills.external_dirs: /mnt/d/Codex_Project/intellectual_tutor/skills`
- verified Hermes can see the repo skill `intellectual-tutor-course-workflow`

Completed in this session:

- confirmed with the user that cost control should use a hybrid inference split
- initially fixed the local deployment target to `Ollama` inside the same `WSL2` environment as the dedicated Hermes instance
- fixed the default local model target to `gemma4:e4b`
- fixed the first local lane scope to:
  simple questions, status explanations, fixed-format helper drafts, and candidate run summaries
- fixed the fallback rule to:
  auto-upgrade local failures or uncertainty to the cloud lane and log the local miss
- fixed the summary/memory rule to:
  keep official Hermes `memory` and `session_search` as the only built-in memory path, with no repo-local clone
- rewrote the opening of `docs/PRD.md` to state the final product goal, core use scenarios, and core product functions explicitly, so new sessions do not read the repo as only a vague single-chapter generator
- aligned the root `README.md` opening summary with the updated PRD so the repository entry point now states the final product as a teacher copilot with Feishu entry, dialogue revision, confirmed preference learning, and cross-chapter continuity
- pushed the hybrid-routing boundary into the runtime-facing repo files:
  `configs/hermes/SOUL.template.md`, `agents/course-app/ProfessorArchitectAgent.md`, and `skills/course/intellectual-tutor-course-workflow/SKILL.md`
- added `configs/hermes/inference_policy.template.yaml` and updated `scripts/bootstrap_hermes_course_app.py` to materialize it into the dedicated `HERMES_HOME`
- added `scripts/check_hybrid_inference.py` so the local lane and fallback-log behavior can be smoke-tested from `WSL2`
- updated `docs/deployment/hermes-wsl2-setup.md` with the repo-specific `Ollama` install and hybrid-lane verification steps
- bootstrapped `/root/.hermes-intellectual-tutor` again so the live instance now includes:
  `SOUL.md` with routing policy and `intellectual_tutor_inference_policy.yaml`
- installed `Ollama 0.21.1` inside `Ubuntu-24.04`, created `/etc/systemd/system/ollama.service`, and verified the service binds `127.0.0.1:11434`
- initialized `AGENT.md` and rewrote `AGENTS.md` so both now point at the current plan-driven resume workflow instead of the earlier stale WSL2/Hermes install pointer
- expanded `AGENTS.md` into a real repository orientation document with:
  read order, layered project map, key entry scripts, key Hermes tools, task-to-file routing, and the default concrete example path under `gradient_descent`
- retried `ollama pull gemma4:e4b` from the dedicated `Ubuntu-24.04` runtime; the pull now gets past manifest resolution and starts a 16-part blob download, but still exits before completion
- captured `journalctl` evidence showing repeated `EOF`, `unexpected EOF`, and intermittent `dial tcp 198.18.0.201/202:443: i/o timeout` while downloading blob `sha256:4c27e0f5b5ad...`
- verified with `curl -Ivs` from `WSL2` that both `https://registry.ollama.ai/v2/` and the signed `r2.cloudflarestorage.com` blob host are TLS-reachable, so the blocker is large-transfer stability rather than basic DNS or certificate failure
- verified that `ollama list` remains empty while partial blob files are accumulating under `/usr/share/ollama/.ollama/models/blobs/`
- removed the failed `sha256:4c27e0f5b5ad...partial*` blob set, restarted `ollama.service`, and reran a clean reinstall attempt for `gemma4:e4b`
- confirmed the clean reinstall progressed much further than earlier attempts, reaching roughly `2.6 GB / 9.6 GB` (`27%`) before the foreground `ollama pull` stopped after about `20` minutes
- confirmed after that retry that `ollama list` is still empty while the partial blob directory is now around `4.0G`
- attempted a one-shot background `nohup` retry, confirmed it was not durable enough, then replaced it with a managed `systemd-run` retry loop
- started `ollama-pull-gemma4-e4b.service` in `WSL2`; it now runs:
  `export HOME=/root; while ! /usr/local/bin/ollama list | grep -q "gemma4:.*e4b"; do /usr/local/bin/ollama pull gemma4:e4b || true; sleep 30; done`
  and currently has a live `/usr/local/bin/ollama pull gemma4:e4b` child process
- verified during the latest heartbeat follow-up that `ollama.service` is still active, `ollama list` still reports no installed models, and a fresh child `/usr/local/bin/ollama pull gemma4:e4b` is again present under `ollama-pull-gemma4-e4b.service`
- verified that the resumable partial blob set remains around `4.0G`; the download is still retrying rather than finishing model registration
- verified in the newest heartbeat that the earlier retry loop is no longer active, `ollama list` is still empty, and a fresh short retry now fails quickly with `Error: EOF`
- captured `journalctl` evidence showing `ollama.service` restarts followed by `total blobs: 0`, so the earlier partial-download progress is no longer the active recovery path
- confirmed the stronger interruption source: `journalctl` shows full `WSL2` shutdown/poweroff sequences during the pull, including
  `Stopping ollama.service`, `Stopped target basic.target`, unmounting `/mnt/c` and `/mnt/d`, `Reached target poweroff.target`, and `Shutting down`
- confirmed from the loop log that a later retry reached about `45%` (`4.3 GB / 9.6 GB`) before being interrupted again, so the pull is capable of progressing but is not surviving the host-side distro shutdown/reboot cycle
- deleted the thread heartbeat automation `retry-gemma4-e4b` at the user's request; there is no longer any automatic background retry in this Codex thread
- after confirming that this machine reclaims `WSL2` even while a transient `systemd` service is still sleeping, changed the approved topology to:
  native Windows `Ollama` plus `WSL2` Hermes, with the Windows endpoint provided to Hermes through `OLLAMA_BASE_URL`
- installed native Windows `Ollama 0.21.1` with `winget`, verified `C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe --version`, verified the local process is running, and confirmed `http://127.0.0.1:11434/api/tags` returns an empty model list before the first Windows-side pull
- attempted the first Windows-side `ollama pull gemma4:e4b`; it progressed much farther than the initial bytes-only phase and reached about `32%` (`3.1 GB / 9.6 GB`) before exiting
- captured `C:\Users\Admin\AppData\Local\Ollama\server.log` evidence showing the same large-blob failure pattern on Windows:
  repeated part stalls plus `unexpected EOF` and `EOF` against the signed `dd20bb891979d25aebc8bec07b2b3bbc.r2.cloudflarestorage.com` blob URL
- this confirms the topology change removed the `WSL2` lifecycle issue from the critical path, but did not remove the host-side network or proxy failure that interrupts large blob transfers
- completed the Windows-side model bring-up after the user finished the install path; `C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe list` now shows `gemma4:e4b`
- reconfigured Windows `ollama.exe serve` with `OLLAMA_HOST=0.0.0.0:11434`, verified Windows now listens on `::`: `11434`, and verified `WSL2` can reach the Windows-hosted endpoint through `http://172.29.0.1:11434/api/tags`
- appended course-app overrides to `/root/.hermes-intellectual-tutor/.env`:
  `OLLAMA_BASE_URL=http://172.29.0.1:11434`
  `LOCAL_FAST_MODEL=gemma4:e4b`
  `CLOUD_PRIMARY_PROVIDER=openrouter`
- ran the repo-side smoke check successfully:
  `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor`
  which passed both the local-lane probe and the fallback-log probe
- switched the repo's documented messaging default from WeCom to Feishu bring-up across the active deployment guide, repo orientation files, plan files, and Hermes config templates so the next session resumes on `FEISHU_APP_ID` / `FEISHU_APP_SECRET` instead of WeCom secrets
- changed the approved local model target from `gemma4:e4b` to `gemma4:26b` across the active repo templates and docs; the current blocker is now that Windows `Ollama` has no installed Gemma 4 model and the user suspects the failed `26b` pull is proxy-related
- verified the live dedicated Hermes instance is already aligned to `gemma4:26b`:
  `/root/.hermes-intellectual-tutor/.env` contains `LOCAL_FAST_MODEL=gemma4:26b`
  `/root/.hermes-intellectual-tutor/intellectual_tutor_inference_policy.yaml` contains `default_model: gemma4:26b`
- reran `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor` and confirmed the current failure mode is `HTTP Error 404: Not Found`, which means `WSL2` reaches the Windows-hosted `Ollama` endpoint but the target model is not installed locally yet
- confirmed the current Windows-side proxy mismatch:
  `HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings` reports `ProxyEnable=1` with `ProxyServer=127.0.0.1:7897`
  but the current `Ollama` `server.log` startup block shows blank `HTTP_PROXY` and `HTTPS_PROXY`

Remaining work:

- verify native Windows `Ollama 0.21.1` remains healthy between retries
- make the Windows `Ollama` process inherit the required proxy path or confirm the proxy is `TUN` / global enough for large blob downloads
- complete `ollama pull gemma4:26b` on Windows
- rerun `scripts/check_hybrid_inference.py` against the dedicated `HERMES_HOME`
- verify automatic fallback logging
- configure live cloud-provider access in `$HERMES_HOME/.env`
- configure Feishu secrets in `$HERMES_HOME/.env`
- start the Hermes gateway and verify Feishu authentication
- run the first allowlisted-user Feishu smoke test
- capture Feishu authentication and smoke-test evidence for later handoff

Current blockers and assumptions:

- the hybrid routing design is now wired into repo templates and smoke-check tooling, but the first local-model pull is not complete yet
- a live cloud provider is still required for high-risk teaching tasks even after the local lane is added
- the local lane must stay outside `lesson_plan`, `quality_review`, source governance, and release gating
- official Hermes memory behavior remains the source of truth for long-term summaries and session recall
- the dedicated runtime should continue using `/root/.hermes-intellectual-tutor` unless the machine setup changes
- the previous `WSL2`-hosted `Ollama` route is now historical evidence rather than the approved path; it was retired because `Ubuntu-24.04` enters a normal `systemd-logind` poweroff path even while background `systemd` services still exist
- that `WSL2` lifecycle issue makes long local-model pulls unreliable inside the distro on this machine
- the current approved path is to host `Ollama` natively on Windows and let Hermes in `WSL2` reach it through `OLLAMA_BASE_URL`
- native Windows `Ollama 0.21.1` is now installed and serving locally, so installation itself is no longer the blocker
- `gemma4:e4b` is now locally available on Windows
- Hermes in `WSL2` reaches the Windows-hosted `Ollama` endpoint through `http://172.29.0.1:11434`
- the repo-side hybrid smoke check now passes, including the fallback-log probe under `/root/.hermes-intellectual-tutor/logs/hybrid_router_fallback.jsonl`
- the live dedicated Hermes instance is already aligned to `gemma4:26b`, so the remaining local-lane blocker is model installation rather than repo/runtime configuration drift
- the active blocker is now the local-model switch to `gemma4:26b`: Windows `Ollama 0.21.1` is installed but no Gemma 4 model is currently available locally, and current evidence points to a proxy mismatch because the machine proxy is enabled while the current `Ollama` service starts with blank `HTTP_PROXY` and `HTTPS_PROXY`
- the keepalive experiment that motivated this topology change was:
  `systemd-run --unit codex-keepalive-test2 --service-type=simple /bin/sleep 300`
  still leaves `wsl.exe -l -v` reporting `Ubuntu-24.04  Stopped` within about `20` seconds, so this machine is not keeping the distro alive solely because a background `systemd` service exists
- there is no active Codex heartbeat automation retrying `gemma4:e4b`; any future retry loop must be started manually
- until `gemma4:26b` is installed locally or a cloud provider is configured and validated, do not claim end-to-end deployment is complete

Verification evidence already captured:

- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'whoami && uname -a && python3 --version'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash -s -- --skip-setup --hermes-home /root/.hermes-intellectual-tutor'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; /root/.hermes-intellectual-tutor/hermes-agent/venv/bin/python /mnt/d/Codex_Project/intellectual_tutor/scripts/bootstrap_hermes_course_app.py --hermes-home /root/.hermes-intellectual-tutor'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; /root/.local/bin/hermes skills list'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; /root/.local/bin/hermes doctor'`
- `python -m py_compile scripts/bootstrap_hermes_course_app.py scripts/check_hybrid_inference.py`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'cd /mnt/d/Codex_Project/intellectual_tutor && python3 scripts/bootstrap_hermes_course_app.py --hermes-home /root/.hermes-intellectual-tutor --overwrite-soul'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'curl -fsSL https://ollama.com/install.sh | sh'` followed by the explicit install/retry path with `zstd`, service creation, and `systemctl enable ollama`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'curl -fsS http://127.0.0.1:11434/api/tags'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'journalctl -u ollama -n 80 --no-pager'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; /usr/local/bin/ollama pull gemma4:e4b'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'journalctl -u ollama -n 120 --no-pager'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'env | grep -i proxy || true; getent ahosts registry.ollama.ai || true; timeout 20 curl -Ivs https://registry.ollama.ai/v2/ 2>&1 || true'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'getent ahosts dd20bb891979d25aebc8bec07b2b3bbc.r2.cloudflarestorage.com || true; timeout 20 curl -Ivs https://dd20bb891979d25aebc8bec07b2b3bbc.r2.cloudflarestorage.com 2>&1 || true'`
- `Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' | Select-Object ProxyEnable,ProxyServer,AutoConfigURL,AutoDetect`
- `netsh winhttp show proxy`
- `winget install --id Ollama.Ollama -e --accept-package-agreements --accept-source-agreements`
- `C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe --version`
- `Invoke-WebRequest -UseBasicParsing -Uri http://127.0.0.1:11434/api/tags -TimeoutSec 10`
- `C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe pull gemma4:e4b`
- `Get-Content "$env:LOCALAPPDATA\Ollama\server.log" | Select-Object -Last 120`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'env | grep -i proxy || true; cat /etc/resolv.conf; getent ahosts registry.ollama.ai | head -n 5'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'systemd-run --unit codex-keepalive-test2 --service-type=simple /bin/sleep 300'`
- `cmd /u /c "wsl.exe -l -v"` after about `20` seconds, confirming `Ubuntu-24.04` is already back to `Stopped` even though the transient service should still have been sleeping
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'ls -lah /usr/share/ollama/.ollama/models; find /usr/share/ollama/.ollama/models/blobs -maxdepth 1 -type f | sed -n "1,40p"'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc '/usr/local/bin/ollama list'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'curl -fsS http://127.0.0.1:11434/api/tags'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'grep -n "LOCAL_FAST_MODEL\|OLLAMA_BASE_URL" /root/.hermes-intellectual-tutor/.env; grep -n "default_model" /root/.hermes-intellectual-tutor/intellectual_tutor_inference_policy.yaml'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor'`
- `Get-Content "$env:LOCALAPPDATA\Ollama\server.log" | Select-Object -Last 80`
- `C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe list`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'ps -ef | grep "[o]llama pull" || true'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'systemctl stop ollama; find /usr/share/ollama/.ollama/models/blobs -maxdepth 1 -type f -name "sha256-4c27e0f5b5ad*" -delete; systemctl start ollama'`
- foreground reinstall evidence: the pull reached roughly `2.6 GB / 9.6 GB` before the CLI returned; re-check with `journalctl -u ollama -n 80 --no-pager`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'du -sh /usr/share/ollama/.ollama/models/blobs; tail -n 20 /root/.hermes-intellectual-tutor/logs/ollama-pull-gemma4-e4b.log 2>/dev/null || true'`
- `wsl.exe -d Ubuntu-24.04 -u root -- systemd-run --unit ollama-pull-gemma4-e4b --service-type=simple /bin/bash -lc 'export HOME=/root; while ! /usr/local/bin/ollama list | grep -q "gemma4:.*e4b"; do date -Is; /usr/local/bin/ollama pull gemma4:e4b || true; sleep 30; done >>/root/.hermes-intellectual-tutor/logs/ollama-pull-gemma4-e4b-loop.log 2>&1'`
- `wsl.exe -d Ubuntu-24.04 -u root -- systemctl status ollama-pull-gemma4-e4b --no-pager`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'ps -ef | grep "[o]llama pull" || true'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'journalctl --since "2026-04-24 11:57:00" --until "2026-04-24 12:27:00" --no-pager | tail -n 200'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'tail -n 80 /root/.hermes-intellectual-tutor/logs/ollama-pull-gemma4-e4b-loop.log 2>/dev/null || true'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'journalctl -u ollama.service -g "Stopped ollama.service\\|Stopping ollama.service\\|Started ollama.service\\|Deactivated successfully" --no-pager'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'journalctl -u ollama -n 80 --no-pager'`
- `wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'timeout 90 /usr/local/bin/ollama pull gemma4:e4b; printf "\nexit=%s\n" "$?"; /usr/local/bin/ollama list'`

## Progress Synchronization Protocol

This plan is the repository source of truth for execution status.

After every meaningful task batch, update this file before ending the session.

Each update should capture:

1. current milestone state
2. completed work
3. remaining work
4. exact next step
5. blockers, assumptions, or environment prerequisites
6. verification commands or evidence when relevant

If the resume point changes, also update:

- `plans/README.md`
- `README.md`
- `docs/README.md`

Do not rely on chat history as the only handoff mechanism.

## Current Milestone Snapshot

- `M1 Hermes Integration Skeleton`: completed in repo
- `M2 Workflow Contract Refactor`: completed in repo
- `M3 Toolization Of Existing Generators`: completed in repo
- `M4 Course Agent And Subagent Setup`: repo-side skeleton completed
- `M5 Run Layout And Release Chain`: completed for local run-based workflow
- `M6 Teacher Change Loop`: completed for local workflow, including structured and legacy compatibility plus PPT regeneration sync
- `M6.5 Hybrid Inference Cost-Control Lane`: repo-side implementation is complete, but the current `gemma4:26b` target is not yet installed locally, so the lane must be re-validated before it is treated as complete on this machine
- `M7 Feishu End-to-End Integration`: in progress; WSL2 distro, official Hermes install, dedicated `HERMES_HOME`, repo-skill mounting, and repo-side hybrid-routing wiring are verified, but live local-model validation, Feishu secrets, and message-path testing are still pending
- `M8 Regression And Local Operations`: partially prepared in docs and in the live machine environment, but not completed as a verified deployed system

## Fixed Architecture

### Official Hermes Core

External to this repository:

- memory, summary, and cleanup mechanisms
- session and adapter framework
- agent runtime
- tool calling and subagent orchestration

### Intellectual Tutor Course App

Owned by this repository:

- course agent and subagent prompts
- workflow contracts
- chapter generation and review tools
- Feishu deployment guidance
- local WSL2 deployment guidance
- Windows-hosted local inference guidance for the WSL2 Hermes instance
- inference routing policy for local vs cloud lanes

### Feishu Entry

The first version uses the official Hermes `Feishu / Lark` adapter directly. This repo does not implement a custom chat gateway.

### Hybrid Inference Lane

The approved cost-control lane is:

- official Hermes memory, `memory` tool, and `session_search` remain the built-in summary and recall system
- native Windows `Ollama + gemma4:26b` serves low-risk requests to the Hermes instance running in `WSL2`
- a live cloud provider remains required for high-risk teaching generation and review

## Milestones

### M1. Hermes Integration Skeleton

Goal: define the repository as a Hermes-loadable course app instead of a standalone script runner.

Delivered:

- `docs/deployment/hermes-wsl2-setup.md`
- `docs/deployment/feishu-setup.md`
- `docs/architecture/course-app-overview.md`
- `configs/hermes/` templates
- `skills/` course skill skeleton
- `agents/` course prompt skeleton

### M2. Workflow Contract Refactor

Goal: express the chapter workflow through structured contracts instead of informal script coupling.

Delivered:

- `schemas/course/lesson_plan.yaml`
- `schemas/course/ppt_script.yaml`
- `schemas/course/notebook_script.yaml`
- `schemas/course/quality_review.yaml`
- `schemas/course/release_manifest.yaml`
- `schemas/course/change_request.yaml`
- `schemas/course/change_confirmation.yaml`

### M3. Toolization Of Existing Generators

Goal: refactor the existing Python generation path into Hermes-callable course tools.

Delivered:

- `tools/lesson_plan_builder.py`
- `tools/ppt_designer.py`
- `tools/notebook_builder.py`
- `tools/verification.py`
- `tools/release_packager.py`
- `tools/status_reader.py`
- `tools/change_applier.py`

### M4. Course Agent And Subagent Setup

Goal: define the course workflow as a Hermes agent system with clear role boundaries.

Delivered:

- course persona and prompt structure
- `Professor Architect Agent`
- `PPT Script Subagent`
- `Notebook Lab Subagent`
- `Quality Review Subagent`
- `Source Curator Subagent`

### M5. Run Layout And Release Chain

Goal: establish run-based outputs and release artifacts aligned with the PRD.

Delivered:

- `outputs/runs/<chapter>/<run_id>/...`
- `review/summary/teacher_summary.md`
- `release_manifest.yaml`
- `source_bundle/debug_index.md`

### M6. Teacher Change Loop

Goal: support propose-change, summarize-change, confirm-change, and scope-aware regeneration.

Delivered:

- `change_request.yaml`
- `change_summary.md`
- `change_confirmation.yaml`
- impact-scope regeneration logic

### M6.5 Hybrid Inference Cost-Control Lane

Goal: reduce cloud cost while keeping high-risk teaching reasoning on the cloud lane.

Remaining deliverables:

- install `gemma4:26b` on Windows `Ollama`
- re-run and preserve smoke-test evidence for the local lane plus cloud fallback

### M7. Feishu End-to-End Integration

Goal: connect the official Hermes Feishu/Lark adapter to the course app.

Remaining deliverables:

- Feishu environment variables and bot config
- local Feishu setup instructions exercised against the live machine
- Feishu smoke-test evidence
- teacher interaction examples through the live channel

### M8. Regression And Local Operations

Goal: make the deployed system repeatable on the current machine.

Remaining deliverables:

- local startup command list
- logging and diagnosis notes
- end-to-end smoke-test writeup
- regression checklist and common-failure guidance

## Recommended Build Order

Proceed in this order:

1. `M1 Hermes Integration Skeleton`
2. `M2 Workflow Contract Refactor`
3. `M3 Toolization Of Existing Generators`
4. `M4 Course Agent And Subagent Setup`
5. `M5 Run Layout And Release Chain`
6. `M6 Teacher Change Loop`
7. `M6.5 Hybrid Inference Cost-Control Lane`
8. `M7 Feishu End-to-End Integration`
9. `M8 Regression And Local Operations`

## Immediate Next Slice

The immediate next slice is no longer `WSL2 official Hermes installation`.

That installation path is complete enough to move into hybrid routing implementation and then live integration.

Execute the next slice in this order:

1. verify native Windows `Ollama 0.21.1` is still installed and the local API responds at `http://127.0.0.1:11434/api/tags`
2. complete `ollama pull gemma4:26b` on Windows
3. verify `/root/.hermes-intellectual-tutor/.env` still contains `OLLAMA_BASE_URL=http://172.29.0.1:11434`
4. set `LOCAL_FAST_MODEL=gemma4:26b` in `/root/.hermes-intellectual-tutor/.env`
5. rerun `python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home /root/.hermes-intellectual-tutor`
6. provide the live cloud-model credentials needed for high-risk Hermes responses
7. provide `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, and optional `FEISHU_ALLOWED_USERS`
8. keep `FEISHU_CONNECTION_MODE=websocket` and `FEISHU_DOMAIN=feishu` for bring-up consistency
9. start `hermes gateway run` or `hermes gateway start` with `HERMES_HOME=/root/.hermes-intellectual-tutor`
10. verify the adapter authenticates successfully to Feishu
11. send the first allowed-user text message through Feishu and confirm Hermes receives and replies

Resume command bundle for the next session:

```bash
winget list --id Ollama.Ollama
Invoke-WebRequest -UseBasicParsing -Uri http://127.0.0.1:11434/api/tags -TimeoutSec 10
C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe list
wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'grep -E "^(OLLAMA_BASE_URL|LOCAL_FAST_MODEL|CLOUD_PRIMARY_PROVIDER)=" /root/.hermes-intellectual-tutor/.env || true'
wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'curl -fsS http://127.0.0.1:11434/api/tags || true'
wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'WINDOWS_HOST=$(awk "/nameserver/ {print \$2; exit}" /etc/resolv.conf); echo "$WINDOWS_HOST"; curl -fsS "http://$WINDOWS_HOST:11434/api/tags" || true'
wsl.exe -d Ubuntu-24.04 -u root -- bash -lc 'export HERMES_HOME=/root/.hermes-intellectual-tutor; python3 /mnt/d/Codex_Project/intellectual_tutor/scripts/check_hybrid_inference.py --hermes-home "$HERMES_HOME"'
```

Only after this slice is verified should the plan advance to broader Feishu smoke coverage and local operations hardening.

## Post-M7 Hardening Intake Rule

This rule activates only after all of the following are recorded in this plan:

- live cloud-provider credentials are validated for the dedicated Hermes instance
- the official Hermes Feishu/Lark adapter authenticates successfully
- the first end-to-end smoke test passes
- reusable verification evidence is captured in this plan

Once those conditions are met:

- do not reopen deployment bring-up work unless regression evidence appears
- do not return to hybrid-lane validation unless the validated local route regresses
- shift the next planning intake to `docs/review/checklist_backlog.md`
- start from `P0` only
- promote selected items into the active planning sources before implementation

The initial post-M7 intake order is:

1. operator self-check and layered diagnostics
2. notebook classroom-safe fallback
3. failure downgrade and human handoff contract
4. minimal cross-artifact acceptance gate
5. teacher-facing status and impact visibility

The required milestone-transition sentence for the M7 completion sync is:

`The bring-up blocker is removed. The next step is no longer deployment validation. The next step is P0 intake from docs/review/checklist_backlog.md.`

## Anti-patterns

- rebuilding Hermes runtime inside this repository
- rebuilding a repo-local memory or summary system that duplicates official Hermes
- letting the Feishu entry call `generate_chapter.py` directly
- turning the course app into a new general-purpose agent platform
- collapsing notebook logic back into the top-level agent
- letting the local model become the primary teaching generator
- skipping `run_id`-based release governance before chat-loop testing
- maintaining two parallel runtimes for Hermes orchestration and repo-local orchestration
