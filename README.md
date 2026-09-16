# Agentic Coder for Codex

Agentic Coder is a skill-only workflow/policy plugin for Codex. It does not replace Codex or make
a model inherently smarter; it changes the execution protocol toward scoped context, disciplined
implementation, diff-first review, evidence-driven verification, and safety checkpoints.

## What it does

It routes work by risk, acquires context progressively, stops when context is sufficient, and
keeps review and verification proportional to the change. It is designed to reduce unnecessary
context/tool usage while preserving correctness; it does not claim measured improvement before a
benchmark demonstrates it.

## Why it exists

Coding agents can spend effort exploring irrelevant files, repeating context, or running ritual
checks. This plugin supplies a compact policy for avoiding those behaviors without adding an API,
runtime service, model wrapper, or external dependency.

## How it works

Simple, Medium, and Complex routes use scope, risk, uncertainty, and reversibility. The policy
follows scope → entry point → relevant dependencies → relevant tests → sufficiency; Medium and
Complex work review the diff before reading surrounding code. Destructive, production, external,
publishing, and irreversible actions require confirmation immediately before execution.

## Installation

```bash
codex plugin marketplace add jafari8001/agentic-coder-codex-plugin --ref v0.3.0
codex plugin add agentic-coder@agentic-coder
```

Open a new Codex thread after installation. The plugin uses the account already configured in the
Codex client and never reads or stores API keys, browser cookies, or passwords.

## Usage

Ask for repository work normally, or say “Use Agentic Coder to …”. The plugin remains policy-only:
it does not autonomously deploy, publish, or communicate externally.

## Evaluation & Benchmarking

v0.3 adds a reproducible benchmark that executes the same synthetic task in isolated Git
workspaces under two conditions: Raw Codex and Codex + Agentic Coder. Fixtures are committed;
generated results are written below `evals/results/` and ignored by Git.

```bash
python3 evals/validate_evals.py
python3 -m unittest discover -s evals/tests
python3 evals/run_benchmark.py --case benchmark-simple-validation
python3 evals/run_benchmark.py --all
python3 evals/report.py evals/results/<run-id>
```

`--condition raw-codex` and `--condition agentic-coder` run one side; the default is comparison.

## Benchmark methodology

Each runnable fixture creates a fresh purpose-built repository, initializes identical Git state,
runs the identical task prompt, captures output/diff/error data, evaluates deterministic acceptance
criteria, and renders per-dimension results. Raw Codex uses `codex exec --ignore-user-config`;
Agentic Coder uses the actually installed plugin. Codex CLI has no explicit per-run plugin selector,
so reports mark comparisons as not fully controlled and record that limitation.

## Metrics

The evaluator reports task success, acceptance checks, tests, changed/unrelated files,
verification, timeout, and execution errors. Tool calls, commands run, files read, and token usage
are recorded as `null` when the CLI does not expose them reliably. Tool/context values are clearly
labelled proxy metrics, never token measurements. Reports compare dimensions without a winner,
ranking, or aggregate score.

## Limitations

Current fixtures are behavioral specifications plus a small synthetic baseline suite. Subjective
requirements and `must_not` prose remain `manual_review_required`; no LLM judge is used. The
runner never fabricates unavailable data or real-agent results.

## Repository structure

```text
plugins/agentic-coder/  Plugin manifest and compact SKILL.md policy
evals/                  Fixtures, validator, benchmark modules, runner, report, tests
.agents/plugins/        Marketplace catalog
```

## Development

Run the fixture validator, infrastructure tests, skill validator, and plugin validator before a
release. The benchmark runner requires an authenticated local Codex CLI and an installed Agentic
Coder plugin for the Agentic condition.

## Versioning / Releases

Update plugin metadata, README release reference, CHANGELOG, and relevant fixtures together. Create
a matching tag such as `v0.3.0`, push it, then create the GitHub Release.

## License

No license file is currently included. Add one before distributing the project under explicit reuse
terms.
