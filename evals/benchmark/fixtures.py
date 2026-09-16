"""Fixture discovery shared by validation and benchmark execution."""

from __future__ import annotations

import json
from pathlib import Path


EVAL_ROOT = Path(__file__).resolve().parents[1]


def load_cases() -> dict[str, dict]:
    cases: dict[str, dict] = {}
    for path in sorted(EVAL_ROOT.rglob("scenarios.json")):
        for case in json.loads(path.read_text(encoding="utf-8")):
            case = {**case, "_fixture_path": str(path.relative_to(EVAL_ROOT))}
            if case["id"] in cases:
                raise ValueError(f"duplicate fixture id: {case['id']}")
            cases[case["id"]] = case
    return cases


def select_cases(case_id: str | None, all_cases: bool) -> list[dict]:
    cases = load_cases()
    if case_id:
        if case_id not in cases:
            raise ValueError(f"unknown case: {case_id}")
        return [cases[case_id]]
    if all_cases:
        return [case for case in cases.values() if "setup" in case]
    raise ValueError("provide --case or --all")
