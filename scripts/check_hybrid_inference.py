from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib import request

import yaml


DEFAULT_POLICY_NAME = "intellectual_tutor_inference_policy.yaml"
DEFAULT_FALLBACK_MODEL = "intellectual-tutor-local-lane-missing"


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data if isinstance(data, dict) else {}


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def call_ollama(*, base_url: str, model: str, prompt: str) -> dict:
    payload = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
    ).encode("utf-8")
    api_url = base_url.rstrip("/") + "/api/chat"
    req = request.Request(
        api_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Smoke-check the Intellectual Tutor hybrid inference lane inside the dedicated Hermes home."
    )
    parser.add_argument("--hermes-home", default=os.environ.get("HERMES_HOME"), help="Target HERMES_HOME path.")
    parser.add_argument("--policy", default=None, help="Optional explicit inference-policy path.")
    parser.add_argument("--ollama-base-url", default=None, help="Optional Ollama base URL override.")
    parser.add_argument("--local-model", default=None, help="Optional local model override.")
    parser.add_argument("--cloud-provider", default=None, help="Optional cloud provider override.")
    parser.add_argument(
        "--prompt",
        default="Reply with exactly: local lane ok",
        help="Prompt for the local-lane reachability check.",
    )
    parser.add_argument(
        "--failure-model",
        default=DEFAULT_FALLBACK_MODEL,
        help="Model name used to force a local-miss log probe.",
    )
    parser.add_argument("--skip-fallback-check", action="store_true", help="Skip the forced local-failure probe.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.hermes_home:
        raise SystemExit("Provide --hermes-home or set HERMES_HOME.")

    hermes_home = Path(args.hermes_home).expanduser()
    env_values = load_env_file(hermes_home / ".env")
    policy_path = Path(args.policy).expanduser() if args.policy else hermes_home / DEFAULT_POLICY_NAME
    policy = load_yaml(policy_path)

    local_lane = policy.get("local_lane", {})
    fallback_policy = policy.get("fallback", {})

    base_url = (
        args.ollama_base_url
        or env_values.get("OLLAMA_BASE_URL")
        or local_lane.get("default_base_url")
        or "http://127.0.0.1:11434"
    )
    local_model = (
        args.local_model
        or env_values.get("LOCAL_FAST_MODEL")
        or local_lane.get("default_model")
        or "gemma4:26b"
    )
    cloud_provider = (
        args.cloud_provider
        or env_values.get("CLOUD_PRIMARY_PROVIDER")
        or fallback_policy.get("default_provider")
        or "openrouter"
    )

    log_path_value = fallback_policy.get("log_path", "logs/hybrid_router_fallback.jsonl")
    log_path = Path(log_path_value)
    if not log_path.is_absolute():
        log_path = hermes_home / log_path

    try:
        response = call_ollama(base_url=base_url, model=local_model, prompt=args.prompt)
    except Exception as exc:  # pragma: no cover - exercised from the CLI
        raise SystemExit(f"Local-lane check failed for model {local_model!r} at {base_url}: {exc}") from exc

    content = response.get("message", {}).get("content", "").strip()
    print("Hybrid local-lane check passed:")
    print(f"- base_url: {base_url}")
    print(f"- local_model: {local_model}")
    print(f"- response_excerpt: {content[:160] or '<empty>'}")

    if args.skip_fallback_check:
        return

    try:
        call_ollama(base_url=base_url, model=args.failure_model, prompt=args.prompt)
    except Exception as exc:  # pragma: no cover - exercised from the CLI
        fallback_entry = {
            "timestamp": utc_now_iso(),
            "event": "local_lane_upgrade_probe",
            "request_class": "status_explanation",
            "local_model": args.failure_model,
            "fallback_reason": str(exc),
            "upgrade_provider": cloud_provider,
            "cloud_call_executed": False,
            "policy_path": str(policy_path),
        }
        append_jsonl(log_path, fallback_entry)
        print("Fallback logging probe passed:")
        print(f"- simulated_local_model: {args.failure_model}")
        print(f"- upgrade_provider: {cloud_provider}")
        print(f"- fallback_log: {log_path}")
        return
    raise SystemExit(
        f"Expected the fallback probe model {args.failure_model!r} to fail, but Ollama accepted it."
    )


if __name__ == "__main__":
    main()
