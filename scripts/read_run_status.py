from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import status_reader


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read a generated run status for Intellectual Tutor.")
    parser.add_argument("--chapter", required=True, help="Chapter id.")
    parser.add_argument("--run-id", required=True, help="Run id.")
    parser.add_argument("--output", default="outputs/runs", help="Run output root.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_root = ROOT / args.output / args.chapter / args.run_id
    summary = status_reader.summarize_run(run_root)
    print("Run status summary:")
    for key, value in summary.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
