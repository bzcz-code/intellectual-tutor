from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


DEFAULT_WSL_SKILLS_DIR = "/mnt/d/Codex_Project/intellectual_tutor/skills"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data if isinstance(data, dict) else {}


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def merge_external_skill_dir(config: dict, skills_dir: str) -> dict:
    merged = dict(config)
    skills_cfg = merged.setdefault("skills", {})
    external_dirs = list(skills_cfg.get("external_dirs", []))
    if skills_dir not in external_dirs:
        external_dirs.append(skills_dir)
    skills_cfg["external_dirs"] = external_dirs
    return merged


def merge_wecom_template(config: dict, template: dict) -> dict:
    merged = dict(config)
    platforms = merged.setdefault("platforms", {})
    template_platforms = template.get("platforms", {})
    for name, value in template_platforms.items():
        if name not in platforms:
            platforms[name] = value
            continue
        if isinstance(platforms[name], dict) and isinstance(value, dict):
            combined = dict(value)
            combined.update(platforms[name])
            platforms[name] = combined
    return merged


def ensure_file_from_template(target: Path, template: Path, *, overwrite: bool) -> None:
    if target.exists() and not overwrite:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap a dedicated Hermes home for the Intellectual Tutor course app.")
    parser.add_argument("--hermes-home", default=os.environ.get("HERMES_HOME"), help="Target HERMES_HOME path.")
    parser.add_argument("--skills-dir", default=DEFAULT_WSL_SKILLS_DIR, help="WSL-visible path to this repo's skills directory.")
    parser.add_argument("--overwrite-soul", action="store_true", help="Overwrite existing SOUL.md from template.")
    parser.add_argument("--overwrite-env", action="store_true", help="Overwrite existing .env from template.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.hermes_home:
        raise SystemExit("Provide --hermes-home or set HERMES_HOME.")

    hermes_home = Path(args.hermes_home).expanduser()
    hermes_home.mkdir(parents=True, exist_ok=True)

    soul_template = ROOT / "configs" / "hermes" / "SOUL.template.md"
    env_template = ROOT / "configs" / "hermes" / "env.template"
    config_template = ROOT / "configs" / "hermes" / "config.template.yaml"

    ensure_file_from_template(hermes_home / "SOUL.md", soul_template, overwrite=args.overwrite_soul)
    ensure_file_from_template(hermes_home / ".env", env_template, overwrite=args.overwrite_env)

    existing_config_path = hermes_home / "config.yaml"
    config = load_yaml(existing_config_path) if existing_config_path.exists() else {}
    config = merge_external_skill_dir(config, args.skills_dir)
    config = merge_wecom_template(config, load_yaml(config_template))
    write_yaml(existing_config_path, config)

    print("Bootstrapped Hermes course app home:")
    print(f"- hermes_home: {hermes_home}")
    print(f"- soul: {hermes_home / 'SOUL.md'}")
    print(f"- env: {hermes_home / '.env'}")
    print(f"- config: {existing_config_path}")
    print(f"- external_skills_dir: {args.skills_dir}")


if __name__ == "__main__":
    main()
