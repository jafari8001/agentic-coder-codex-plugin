# Agentic Coder evaluations

These JSON fixtures specify expected Agent behaviour; they are not model calls, application tests,
model benchmarks, or token benchmarks. Each scenario records category, route, context behaviour,
verification, safety, prohibited behaviour, and notes.

Run `python3 evals/validate_evals.py` to validate the fixtures. For a manual regression pass, give
each `task` to Codex with Agentic Coder enabled and compare observable behaviour with the expected
fields. The format permits future observed-versus-expected execution data without implementing a
runner now. Do not require literal wording or a fixed command sequence.
