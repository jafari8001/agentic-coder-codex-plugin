"""Run one or more reproducible Raw Codex / Agentic Coder benchmark cases."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from benchmark.evaluation import compare, evaluate
from benchmark.execution import execute
from benchmark.fixtures import select_cases
from benchmark.reporting import write_report
from benchmark.workspace import prepare


def version(command: list[str]) -> str | None:
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--case")
    selector.add_argument("--all", action="store_true")
    parser.add_argument("--condition", choices=("raw-codex", "agentic-coder", "comparison"), default="comparison")
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--results-dir", type=Path, default=Path(__file__).parent / "results")
    args = parser.parse_args()
    run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    destination = args.results_dir / run_id
    destination.mkdir(parents=True)
    conditions = ("raw-codex", "agentic-coder") if args.condition == "comparison" else (args.condition,)
    result = {"metadata": {"benchmark_version": "0.3.0", "runner_version": "0.3.0", "git_commit": version(["git", "rev-parse", "HEAD"]), "plugin_version": "0.3.0", "codex_version": version(["codex", "--version"]), "model": args.model, "timeout": args.timeout, "controlled_comparison": False, "comparison_limitation": "Codex CLI exposes no explicit plugin selector: raw uses --ignore-user-config while Agentic Coder uses the installed plugin configuration."}, "cases": {}}
    for case in select_cases(args.case, args.all):
        case_result = {"fixture": case["_fixture_path"], "runs": {}, "evaluations": {}}
        for condition in conditions:
            with prepare(case) as temporary:
                root = Path(temporary)
                run = execute(case, condition, root, destination / case["id"] / condition, args.model, case.get("timeout", args.timeout))
                case_result["runs"][condition] = run
                case_result["evaluations"][condition] = evaluate(case, run, root)
        raw_run = case_result["runs"].get("raw-codex", {})
        agentic_run = case_result["runs"].get("agentic-coder", {})
        raw = {**raw_run, **case_result["evaluations"].get("raw-codex", {}), **raw_run.get("metrics", {})}
        agentic = {**agentic_run, **case_result["evaluations"].get("agentic-coder", {}), **agentic_run.get("metrics", {})}
        case_result["comparison"] = compare(raw, agentic)
        case_result["manual_review_required"] = any(item.get("manual_review_required") for item in case_result["evaluations"].values())
        result["cases"][case["id"]] = case_result
    (destination / "metadata.json").write_text(json.dumps(result["metadata"], indent=2), encoding="utf-8")
    (destination / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_report(result, destination)
    print(destination)


if __name__ == "__main__":
    main()
