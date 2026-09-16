from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVALS))

from benchmark.evaluation import compare, evaluate
from benchmark.fixtures import load_cases
from benchmark.reporting import render
from benchmark.workspace import prepare


class BenchmarkInfrastructureTest(unittest.TestCase):
    def test_runnable_fixture_workspace_and_evaluation(self) -> None:
        case = load_cases()["benchmark-simple-validation"]
        with prepare(case) as temporary:
            root = Path(temporary)
            target = root / "validator.py"
            target.write_text("def valid(value):\n    return value >= 0\n", encoding="utf-8")
            run = {"exit_status": 0, "files_changed": ["validator.py"]}
            result = evaluate(case, run, root)
        self.assertTrue(result["task_success"])
        self.assertTrue(result["tests_passed"])

    def test_comparison_keeps_unavailable_metrics_null(self) -> None:
        comparison = compare({"files_changed": ["a"], "tool_calls": None}, {"files_changed": [], "tool_calls": None})
        self.assertEqual(comparison["files_changed"], {"raw-codex": 1, "agentic-coder": 0})
        self.assertEqual(comparison["tool_calls"], {"raw-codex": None, "agentic-coder": None})

    def test_report_is_machine_result_renderable(self) -> None:
        result = {"metadata": {"benchmark_version": "0.3.0", "controlled_comparison": False}, "cases": {"case": {"comparison": {"tool_calls": {"raw-codex": None, "agentic-coder": None}}, "manual_review_required": True}}}
        self.assertIn("tool_calls", render(result))
