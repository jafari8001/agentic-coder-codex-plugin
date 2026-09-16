# Agentic Coder evaluations

These JSON fixtures specify expected Agent behaviour. Runnable fixtures additionally provide
synthetic setup and deterministic acceptance criteria for the benchmark runner. They are not model
benchmarks or token benchmarks; unavailable CLI metrics remain `null`.

Run `python3 evals/validate_evals.py` to validate the fixtures. For a manual regression pass, give
each `task` to Codex with Agentic Coder enabled and compare observable behaviour with the expected
fields. Run runnable fixtures with `python3 evals/run_benchmark.py --all`; results are ignored by
Git. Do not require literal wording or a fixed command sequence.
