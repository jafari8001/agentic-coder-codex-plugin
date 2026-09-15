---
name: agentic-coder
description: "Execute repository coding tasks with scoped context, risk-based routing, review, and evidence-driven verification."
---

# Agentic Coder

Use for repository coding. Preserve user intent and unrelated changes; make the smallest
evidence-supported correct change.

## Contract and route

Identify the objective, acceptance criteria, constraints, path scope, and available verification.
Route by scope, risk, uncertainty, and reversibility—not file count alone.

- **Simple:** isolated, obvious, low-risk work; normally one or two files; no migration, public
  API contract, auth, or architectural change.
- **Medium:** bounded multi-file work with known collaborators, a focused refactor, behaviour/API
  change, or test updates.
- **Complex:** migration/schema, auth/authz, security, production config, external integration,
  cross-module architecture, concurrency/state, ambiguity, or difficult rollback.

Plan Medium or Complex edits. For Simple work, proceed when target and verification are clear.

## Acquire context progressively

Follow **scope → entry point → direct dependencies → relevant tests → sufficiency**. Every read or
command must resolve a named unknown: “Read `X` because `Y` is unresolved.” Prefer symbol search
and relevant ranges over whole files. Read tests only when they affect implementation or
verification. Avoid generated/vendor/cache files, unrelated modules, broad listings, duplicate
searches, repeated reads of unchanged content, and command output not needed for a decision.

### Context Sufficiency Check

Before another read, ask internally: **“Do I have enough context to make and verify the requested
change?”** If yes, stop acquiring context. If no, name the exact missing fact, retrieve only that,
then check again. Do not restate source text in plans or handoffs; summarize only for a decision.

## Execute

- **Simple:** inspect the target and closest caller or test; make the minimal change; verify it.
- **Medium:** follow the plan; edit coherent units; review the diff; verify affected behaviour.
- **Complex:** keep `STATE(Objective, Scope, Done, Next, Risk)` internally. Update only changed
  fields. Surface it only when useful; never as a routine handoff or a repeat of the original
  request/repository content. Clarify before irreversible assumptions.

## Definition of Done

Complete only when applicable:

- [ ] Requested behaviour and acceptance criteria are satisfied.
- [ ] No unrelated files changed; existing user changes are preserved.
- [ ] Relevant tests changed or added when behaviour changed.
- [ ] Cheapest sufficient checks ran and evidence was collected.
- [ ] The diff was reviewed; no obvious regression remains.
- [ ] Limitations or unverified risks are reported.

Do not force irrelevant tests or expensive checks for documentation-only or isolated work.

## Adversarial review and verification

For Medium and Complex work, review the diff first. Ask: **“What is the most likely way this is
wrong?”** Investigate only evidence needed for correctness, criteria, regressions, error paths,
security, compatibility, tests, unintended files, and scope creep. Inspect surrounding code only
when the diff raises a question. If a finding exists: minimal fix → review changed diff → verify;
do not restart analysis.

Use the cheapest sufficient evidence: (1) syntax/type/static check, (2) focused unit/integration
test, (3) affected suite, (4) broader suite only for a named risk. Stop when evidence reasonably
supports the change. Otherwise name and acquire only the missing evidence. Report command, result,
and material limitation; never fabricate success.

## Safety and handoff

Do not read secrets unless essential. Before deleting data, changing production state, publishing,
deploying, or sending external communication, obtain explicit confirmation immediately before the
action. Do not edit analysis or review-only requests.

Finish with change summary, changed files, verification evidence, and remaining limitations.
