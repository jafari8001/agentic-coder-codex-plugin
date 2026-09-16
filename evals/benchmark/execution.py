"""Run Codex and capture only metrics the CLI can actually expose."""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

from .workspace import changed_files, git_output


def agentic_plugin_available() -> bool:
    completed = subprocess.run(["codex", "plugin", "list"], capture_output=True, text=True)
    return completed.returncode == 0 and "agentic-coder@agentic-coder" in completed.stdout


def execute(case: dict, condition: str, root: Path, output_dir: Path, model: str | None, timeout: int) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    final_path = output_dir / "final.md"
    stdout_path = output_dir / "events.jsonl"
    stderr_path = output_dir / "stderr.log"
    plugin_available = agentic_plugin_available() if condition == "agentic-coder" else None
    if condition == "agentic-coder" and not plugin_available:
        return {"condition": condition, "exit_status": None, "execution_error": "Agentic Coder plugin is not installed", "timeout": False, "metrics": unavailable_metrics(), "final_response": None}
    command = ["codex", "exec", "--json", "--ephemeral", "--sandbox", "workspace-write", "-C", str(root), "-o", str(final_path)]
    if condition == "raw-codex":
        command.append("--ignore-user-config")
    if model:
        command.extend(["--model", model])
    command.append(case["task"])
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        stdout_path.write_text(completed.stdout, encoding="utf-8")
        stderr_path.write_text(completed.stderr, encoding="utf-8")
        error = completed.stderr.strip() if completed.returncode else None
        timed_out = False
        status = completed.returncode
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_text(exc.stdout or "", encoding="utf-8")
        stderr_path.write_text(exc.stderr or "", encoding="utf-8")
        error, timed_out, status = "timeout", True, None
    except (OSError, UnicodeError) as exc:
        stdout_path.write_text("", encoding="utf-8")
        stderr_path.write_text(str(exc), encoding="utf-8")
        error, timed_out, status = str(exc), False, None
    return {
        "condition": condition,
        "started_at": started,
        "ended_at": time.time(),
        "exit_status": status,
        "execution_error": error,
        "timeout": timed_out,
        "final_response": final_path.read_text(encoding="utf-8") if final_path.exists() else None,
        "files_changed": changed_files(root),
        "git_diff": git_output(root, "diff"),
        "git_diff_stat": git_output(root, "diff", "--stat"),
        "command": command,
        "plugin_available": plugin_available,
        "metrics": unavailable_metrics(),
    }


def unavailable_metrics() -> dict:
    return {
        "tool_calls": None,
        "commands_run": None,
        "files_read": None,
        "unnecessary_exploration": None,
        "token_usage": None,
        "proxy_metrics": ["tool_calls", "commands_run", "files_read"],
    }
