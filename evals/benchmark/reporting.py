"""Render comparison data without ranking conditions or inventing metrics."""

from __future__ import annotations

from pathlib import Path


def render(result: dict) -> str:
    lines = ["# Agentic Coder benchmark report", "", f"- Benchmark version: {result['metadata']['benchmark_version']}", f"- Controlled comparison: {result['metadata']['controlled_comparison']}", "- Metrics unavailable from the CLI are recorded as `null`; tool/context values are proxy metrics, not token measurements.", ""]
    for case_id, case in result["cases"].items():
        lines += [f"## {case_id}", "", "| Metric | Raw Codex | Agentic Coder |", "| --- | --- | --- |"]
        for metric, values in case["comparison"].items():
            lines.append(f"| {metric} | {values['raw-codex']} | {values['agentic-coder']} |")
        lines += ["", f"Manual review required: {case['manual_review_required']}", ""]
    return "\n".join(lines)


def write_report(result: dict, directory: Path) -> Path:
    path = directory / "report.md"
    path.write_text(render(result), encoding="utf-8")
    return path
