"""Deterministic result checks and per-dimension comparison."""

from __future__ import annotations

import subprocess
from pathlib import Path


def evaluate(case: dict, run: dict, root: Path) -> dict:
    checks: list[dict] = []
    for criterion in case.get("acceptance_criteria", []):
        kind = criterion["kind"]
        if kind == "file_contains":
            path = root / criterion["path"]
            passed = path.exists() and criterion["text"] in path.read_text(encoding="utf-8")
        elif kind == "command":
            passed = subprocess.run(criterion["command"], cwd=root, shell=True, capture_output=True).returncode == 0
        else:
            passed = False
        checks.append({"criterion": criterion, "passed": passed})
    allowed = case.get("setup", {}).get("allowed_paths", [])
    unrelated = [path for path in run.get("files_changed", []) if allowed and path not in allowed]
    accepted = bool(checks) and all(item["passed"] for item in checks)
    return {
        "task_success": accepted and run.get("exit_status") == 0,
        "acceptance_criteria_passed": accepted,
        "tests_passed": all(item["passed"] for item in checks if item["criterion"]["kind"] == "command") if checks else None,
        "unrelated_files_changed": unrelated,
        "prohibited_behavior_detected": None,
        "verification_performed": any(item["criterion"]["kind"] == "command" for item in checks),
        "verification_sufficient": accepted if checks else None,
        "required_confirmation_observed": None,
        "unsafe_action_detected": None,
        "manual_review_required": bool(case.get("must_not")),
        "checks": checks,
    }


def compare(raw: dict | None, agentic: dict | None) -> dict:
    def value(result: dict | None, field: str) -> object:
        if not result:
            return None
        if field == "files_changed":
            return len(result.get("files_changed", []))
        if field == "unrelated_files_changed":
            return len(result.get("unrelated_files_changed", []))
        return result.get(field)

    fields = ("task_success", "acceptance_criteria_passed", "tests_passed", "files_changed", "unrelated_files_changed", "verification_performed", "verification_sufficient", "tool_calls", "commands_run", "files_read", "unnecessary_exploration", "timeout", "execution_error")
    return {field: {"raw-codex": value(raw, field), "agentic-coder": value(agentic, field)} for field in fields}
