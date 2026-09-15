---
name: agentic-coder
description: "Run a disciplined, context-efficient coding workflow: classify scope, inspect only necessary files, plan when warranted, implement minimal changes, review, and verify."
---

# Agentic Coder

Use this skill for repository coding tasks when the user asks to implement, modify, refactor,
debug, review, or verify code. The goal is a minimal correct change with visible evidence, not a
long explanation or broad rewrite.

## Operating rules

1. Treat the user's request as the task contract. Identify the objective, acceptance criteria,
   allowed paths, constraints, and verification commands before editing.
2. Never read an entire repository by default. First inspect the file tree, locate likely entry
   points with targeted search, then read only the relevant declarations and direct tests.
3. Preserve unrelated user changes. Do not reset, discard, or reformat files outside the task.
4. Do not expose credentials or read private configuration unless it is essential to the task.
5. Make changes only in the current repository and only after confirming the target paths.
6. Prefer the repository's existing style, dependencies, and test conventions.

## Choose the route

Classify the task before implementation.

### Simple

Use this route for an isolated, low-risk change whose affected file and behaviour are obvious.

1. Read the target declaration and its closest test or caller.
2. Implement the smallest complete change.
3. Run the most focused relevant check.
4. Report changed files, verification evidence, and any limitation.

### Medium

Use this route for a bounded multi-file change with known behaviour.

1. Extract only the required context: entry point, direct collaborators, configuration, and tests.
2. State a short ordered plan with affected paths and verification for each meaningful step.
3. Implement the plan in small coherent edits.
4. Review the resulting diff against the task contract.
5. Run focused checks and report their exact outcome.

### Complex

Use this route for cross-cutting, ambiguous, security-sensitive, stateful, migration, or
high-impact work.

1. Analyze minimal context first. Build a map of the relevant entry points, data flow, callers,
   tests, and constraints. If context is insufficient, ask a concise clarification before making
   irreversible assumptions.
2. Produce an ordered plan with dependencies, path-level scope, risks, rollback considerations,
   and verification commands.
3. Before every substantial implementation step, restate the compact handoff: objective,
   constraints, selected files, completed plan steps, and unresolved risks. Do not repeat source
   text that is still available from the repository.
4. Implement only the approved scope. Keep diffs small and avoid opportunistic refactors.
5. Review independently for correctness, acceptance criteria, compatibility, security, error
   paths, tests, and unintended file changes.
6. Run verification. If a check cannot run, say exactly why and provide the command the user can
   run locally.

## Implementation and review standards

- Show a concise plan before medium or complex edits.
- Use existing tests where possible; add or update a focused test when behaviour changes.
- Validate generated code, configuration, and migrations with the project-native tooling.
- For every modified file, explain its purpose in one sentence in the final response.
- If the task asks only for analysis or review, do not modify files.
- If a requested action could delete data, change production state, publish artifacts, or send
  external communication, obtain explicit confirmation immediately before that action.

## Final handoff

Return only the information needed to review the result:

1. What changed and why.
2. Files changed.
3. Verification commands and outcomes.
4. Remaining risks, missing context, or follow-up work.

When no change was made, clearly state why and what is needed to proceed.
