---
name: openviking-mini-tester
description: Test openviking-mini changes. Use when discovering test commands, writing or running focused tests, verifying TDD behavior, checking full-suite readiness, or reporting test risk for this minimal OpenViking architecture learning project.
---

# openviking-mini Tester Skill

Use this skill whenever tests are added, changed, or run in `openviking-mini`.

## Principles

- Test behavior through documented interfaces.
- Prefer deterministic tests that do not require network access or external services.
- Keep test scope narrow for small changes.
- Treat missing tests as a project risk, not a passing result.

## Discovery Workflow

1. Read `AGENTS.md`.
2. Inspect project files to identify the language, package manager, and test runner.
3. Prefer existing test commands over introducing a new runner.
4. If no test runner exists, recommend the smallest test setup needed for the current implementation language.

## TDD Workflow

1. Confirm the relevant docs and interface contract exist.
2. Add or inspect a failing test that describes the intended behavior.
3. Run the focused test and confirm it fails for the expected reason when possible.
4. Implement or inspect the smallest code needed.
5. Run the focused test again.
6. Run broader tests when shared behavior changed.

## Reporting

Report:

- The exact test command used.
- Whether focused tests passed.
- Whether full tests passed or were unavailable.
- Any skipped, missing, flaky, or environment-dependent test risk.

Do not claim the project is verified if only static inspection happened.

## Red Flags

- Tests require real external services for core behavior.
- Tests only check file existence or implementation details.
- Tests pass without exercising the documented interface.
- New behavior has no failure-path test.
- A failing test is ignored to finish faster.
