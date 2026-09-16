"""Create deterministic disposable Git workspaces from fixture setup files."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def prepare(case: dict) -> tempfile.TemporaryDirectory[str]:
    setup = case.get("setup")
    if not setup:
        raise ValueError(f"{case['id']} has no runnable setup")
    temporary = tempfile.TemporaryDirectory(prefix=f"agentic-coder-{case['id']}-")
    root = Path(temporary.name)
    for item in setup.get("files", []):
        path = root / item["path"]
        if path.resolve().parent != root.resolve() and root.resolve() not in path.resolve().parents:
            raise ValueError(f"unsafe fixture path: {item['path']}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(item["content"], encoding="utf-8")
    for command in (
        ["git", "init", "-q"],
        ["git", "add", "."],
        ["git", "-c", "user.name=Benchmark", "-c", "user.email=benchmark@example.invalid", "commit", "-qm", "baseline"],
    ):
        subprocess.run(command, cwd=root, check=True, capture_output=True, text=True)
    return temporary


def git_output(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout


def changed_files(root: Path) -> list[str]:
    return [line[3:] for line in git_output(root, "status", "--short").splitlines()]
