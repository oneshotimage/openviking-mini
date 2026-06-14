---
name: openviking-mini-review
description: Review and test openviking-mini changes. Use when working in this repository to check documentation-first development, explicit interfaces, TDD discipline, minimal OpenViking context-database scope, supporting capability boundaries, and runnable tests before code is accepted.
---

# openviking-mini Review Skill

Use this skill before accepting code changes in `openviking-mini`.

## Inputs

- The current diff.
- `AGENTS.md`.
- Relevant docs under `docs/`.
- Relevant tests and source files.

## Review Workflow

1. Read `AGENTS.md` first.
2. Inspect the diff and identify changed docs, interfaces, tests, and runtime code.
3. Confirm docs were added or updated for behavior and interface changes.
4. Confirm the change maps to an OpenViking core capability.
5. Confirm supporting boundaries remain explicit: context types, native operations, ingestion, model adapters, intent analysis, and security/privacy.
6. Confirm interfaces are explicit and small.
7. Confirm tests cover normal behavior and at least one failure path for new interfaces.
8. Run the narrowest relevant test command.
9. Report findings before summaries.

## Test Workflow

1. Discover the project test runner from existing files.
2. If no runner exists yet, say so and recommend the smallest runner needed for the current language.
3. Run focused tests first.
4. Run the full suite when it exists and the change touches shared behavior.
5. Treat skipped or unavailable tests as review risk, not success.

## Findings Format

Lead with actionable findings ordered by severity. Include file and line references when possible.

If no issues are found, say that clearly and mention the exact test command that passed.

## Red Flags

- Runtime code appears before docs or interfaces.
- New code is unrelated to the OpenViking context database / memory base core.
- Context types are collapsed into one opaque document bucket.
- Model calls are embedded directly in stores, retrievers, or domain models.
- Retrieval crosses user, peer, private resource, or context type boundaries without an explicit access rule.
- Large scaffolding hides the core idea.
- Tests assert implementation trivia instead of behavior.
- Interfaces accept or return unstructured dictionaries without a documented boundary reason.
- External services are required for deterministic core tests.
