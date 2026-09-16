# Changelog

All notable changes to this plugin are documented in this file.

## 0.3.0 — 2026-09-16

### Added

- Dependency-free benchmark runner, isolated synthetic workspaces, structured observations, and
  Markdown reporting for Raw Codex versus Agentic Coder.

### Changed

- Extends eval fixtures with optional runnable setup and deterministic acceptance criteria.
- Adds infrastructure tests and ignores generated benchmark results.

### Documentation

- Documents methodology, metrics, limitations, and the v0.3.0 release workflow.

## 0.2.2 — 2026-09-16

- Hardens context sufficiency, compact state, diff-first review, and evidence-driven verification.
- Aligns release metadata on version 0.2.2 and removes the local development cachebuster.
- Updates behavioral fixtures for expected context, verification, and safety behavior; adds review
  and verification coverage without an execution harness.

## 0.2.1 — 2026-09-15

- Aligns release metadata and the installation example on version 0.2.1.
- Refines Complex-task state so unchanged context is not surfaced as a routine handoff.
- Retains progressive context acquisition, diff-first review, and lightweight behavioral fixtures.

## 0.2.0 — 2026-09-15

- Adds progressive context acquisition and an explicit Context Sufficiency Check.
- Clarifies risk-based Simple, Medium, and Complex routing.
- Adds Definition of Done, compact Complex state, diff-first adversarial review, and a cheapest-
  sufficient verification strategy.
- Adds lightweight behavioral evaluation fixtures and a dependency-free format validator.

## 0.1.0 — 2026-09-15

- Initial public release of the Agentic Coder skill-only Codex plugin.
- Adds simple, medium, and complex coding workflows with scoped context, planning, review, and
  verification guidance.
- Requires no API key, browser cookie, or external service; the signed-in Codex client supplies
  the model and account access.
