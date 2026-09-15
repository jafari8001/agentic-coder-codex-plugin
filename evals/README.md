# Agentic Coder evaluations

These JSON fixtures define expected workflow behaviour; they are not model calls or application
tests. Each scenario specifies route, scope, verification, prohibited behaviour, and safety.

Run `python3 evals/validate_evals.py` to validate the fixtures. For a manual regression pass, give
each `task` to Codex with Agentic Coder enabled and compare its observable workflow with the other
fields. Do not require literal wording or a fixed command sequence.
