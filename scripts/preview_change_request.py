from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import change_applier


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preview a structured teacher change request.")
    parser.add_argument("--request", required=True, help="Path to change_request.yaml")
    parser.add_argument("--output", default=None, help="Optional output markdown path for the summary.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    request_path = Path(args.request)
    with request_path.open("r", encoding="utf-8") as handle:
        request = yaml.safe_load(handle)
    lines = change_applier.build_change_summary(request)
    if args.output:
        change_applier.write_change_summary(lines, Path(args.output))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
