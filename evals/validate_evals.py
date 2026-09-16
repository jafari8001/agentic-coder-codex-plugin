"""Validate the lightweight Agentic Coder evaluation-fixture schema."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent
REQUIRED_FIELDS = {
    "id",
    "category",
    "task",
    "expected_route",
    "expected_context_behavior",
    "expected_verification",
    "expected_safety_behavior",
    "must_not",
    "notes",
}
VALID_ROUTES = {"simple", "medium", "complex"}
VALID_CATEGORIES = {"routing", "context_efficiency", "review", "verification", "safety"}


def main() -> None:
    errors: list[str] = []
    scenario_ids: set[str] = set()
    for path in sorted(ROOT.rglob("*.json")):
        try:
            scenarios = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({error.msg})")
            continue
        if not isinstance(scenarios, list) or not scenarios:
            errors.append(f"{path.relative_to(ROOT)}: expected a non-empty list")
            continue
        for index, scenario in enumerate(scenarios, start=1):
            label = f"{path.relative_to(ROOT)}[{index}]"
            if not isinstance(scenario, dict):
                errors.append(f"{label}: expected an object")
                continue
            missing = REQUIRED_FIELDS - scenario.keys()
            if missing:
                errors.append(f"{label}: missing {', '.join(sorted(missing))}")
            if scenario.get("expected_route") not in VALID_ROUTES:
                errors.append(f"{label}: invalid expected_route")
            if scenario.get("category") not in VALID_CATEGORIES:
                errors.append(f"{label}: invalid category")
            scenario_id = scenario.get("id")
            if not isinstance(scenario_id, str) or not scenario_id:
                errors.append(f"{label}: id must be a non-empty string")
            elif scenario_id in scenario_ids:
                errors.append(f"{label}: duplicate id {scenario_id}")
            else:
                scenario_ids.add(scenario_id)
            for field in {"expected_context_behavior", "expected_verification", "must_not"}:
                value = scenario.get(field)
                if not isinstance(value, list) or not value or not all(
                    isinstance(item, str) and item for item in value
                ):
                    errors.append(f"{label}: {field} must be a non-empty list of strings")
            for field in {"task", "expected_safety_behavior", "notes"}:
                value = scenario.get(field)
                if not isinstance(value, str) or not value:
                    errors.append(f"{label}: {field} must be a non-empty string")
    if errors:
        raise SystemExit("Evaluation fixture validation failed:\n- " + "\n- ".join(errors))
    print(f"Validated {len(scenario_ids)} evaluation scenarios.")


if __name__ == "__main__":
    main()
