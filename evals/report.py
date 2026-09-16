"""Render a Markdown report from a completed benchmark results.json file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmark.reporting import write_report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="results directory or results.json")
    args = parser.parse_args()
    source = args.results if args.results.name == "results.json" else args.results / "results.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    print(write_report(data, source.parent))


if __name__ == "__main__":
    main()
