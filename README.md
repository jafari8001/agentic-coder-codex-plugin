# Agentic Coder for Codex

Agentic Coder is a skill-only Codex plugin for disciplined repository work. It uses the Codex
client and the account already signed in there; it does not request, store, or transmit an OpenAI
API key.

The skill uses a compact engineering protocol: progressive context acquisition, risk-based routing,
minimal implementation, adversarial diff review, and evidence-driven verification. It asks for
confirmation before destructive or external actions.

## Workflow

- **Simple / Medium / Complex:** routes work by scope, risk, uncertainty, and reversibility—not
  file count alone.
- **Context Sufficiency Check:** before every additional read, Codex asks whether it has enough
  context to make and verify the change. If not, it retrieves only the named missing fact.
- **Definition of Done:** requires applicable acceptance criteria, focused verification, diff
  review, preserved user changes, and explicit limitations.
- **Adversarial review:** Medium and Complex work review the diff first, then inspect surrounding
  code only where the diff raises a concrete question.
- **Verification:** starts with the cheapest sufficient check and expands only for a known risk.

## Evaluations

[`evals/`](./evals) contains lightweight behavioral fixtures for routing, context efficiency,
verification, and safety. They are not application tests and do not call a model. Validate their
format with:

```bash
python3 evals/validate_evals.py
```

## Install from a checkout

Clone this repository, then add its marketplace directory to Codex and install the plugin:

```bash
codex plugin marketplace add /absolute/path/to/agentic-coder-codex-plugin
codex plugin add agentic-coder@agentic-coder
```

Start a new Codex thread after installation, then ask for a coding task normally or say “Use
Agentic Coder to …”. Codex runs the skill with the account and usage allowance already configured
in the official client.

## Install from a public Git repository

After a maintainer publishes a tagged release, install that immutable release rather than a moving
branch. Replace `OWNER/REPO` with the published Git repository:

```bash
codex plugin marketplace add OWNER/REPO --ref v0.2.1
codex plugin add agentic-coder@agentic-coder
```

To update an installed Git marketplace after a newer release is published:

```bash
codex plugin marketplace upgrade agentic-coder
```

Open a new Codex thread after installing or updating so the current skill instructions load.

## What it does not do

This package is intentionally not a wrapper around an API. It does not read browser cookies,
passwords, ChatGPT session tokens, or API keys. It also does not use LiteLLM; the signed-in Codex
client supplies the model and tools.

## Release process

1. Update `plugins/agentic-coder/.codex-plugin/plugin.json`, `CHANGELOG.md`, and relevant evals with the next
   semantic version.
2. Validate the skill and plugin:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py \
  plugins/agentic-coder/skills/agentic-coder

python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/agentic-coder
```

3. Commit the release, create a matching Git tag such as `v0.2.1`, push the tag, and create a
   GitHub Release from it.

The marketplace manifest at `.agents/plugins/marketplace.json` is the root catalog used by Codex.
Keep the plugin name and its source path stable after publication so existing installations can
upgrade safely.
