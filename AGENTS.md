# AGENTS.md

This repository is `openviking-mini`: a learning project for understanding the architecture principles of OpenViking by building the smallest runnable version of its core behavior.

## Mission

- Explain architecture through working code, tests, and short documents.
- Implement only the minimum OpenViking-like core needed to demonstrate the architecture.
- Prefer clarity over completeness. Every module must be easy to read and justify.

## Hard Boundaries

- Do not copy proprietary OpenViking source code.
- Do not generate unrelated product features, UI pages, integrations, demo fillers, mock SaaS screens, or broad framework scaffolding.
- Do not create large unreadable files or speculative abstractions.
- Do not implement secondary systems before the core architecture is documented and tested.
- Do not add dependencies unless they remove meaningful complexity for the minimal core.
- Do not hide behavior behind magic global state.

## Required Workflow

1. Write or update documentation before implementation.
2. Define interfaces before implementation details.
3. Write failing tests before production code.
4. Implement the smallest code that makes the tests pass.
5. Refactor only after tests pass and the architecture remains easier to explain.
6. Add or update an example that demonstrates the finished feature.
7. Review the diff against this file before finishing.

## Documentation First

Before adding runtime code, create or update concise docs under `docs/`.

Required docs for core work:

- `docs/architecture.md`: core components, responsibilities, data flow, and why the split exists.
- `docs/interfaces.md`: public interfaces, input/output contracts, error behavior, and extension points.
- `docs/testing.md`: test strategy and how to run tests.

Docs must stay close to the implementation. If code changes an interface or responsibility, update the docs in the same change.

## Architecture Shape

The minimal implementation should separate these concerns:

- Domain model: pure data and invariants.
- Planner or orchestrator: decides the next action from state and available tools.
- Tool interface: describes callable capabilities without binding to a specific provider.
- Runtime loop: executes planner decisions and records results.
- Persistence boundary: optional, explicit, and replaceable.

Keep the first version in-process and deterministic unless a test proves a boundary is needed.

## Interface Rules

- Public interfaces must be typed or otherwise explicit.
- Inputs, outputs, and errors must be documented before implementation.
- Prefer small protocols, interfaces, or dataclasses over loose dictionaries.
- Keep serialization at system boundaries, not inside domain logic.
- New interfaces require tests for normal behavior and at least one failure path.

## TDD Rules

- Add tests first for every behavior change.
- A test should describe architecture behavior, not incidental implementation details.
- Prefer deterministic unit tests for the core.
- Add integration tests only when component boundaries need proof.
- Do not skip tests silently. If a test cannot run, document why in the final response.

## Example Rules

- Every completed feature must include one runnable example under `examples/`.
- Examples must demonstrate the public interface, not private implementation details.
- Examples must be short enough to read in one sitting.
- Examples must avoid unrelated product behavior, external services, and decorative output.
- If an example stops matching an interface, update the example in the same change.

## Code Size Rules

- Start with one narrow vertical slice.
- Keep files small enough to review comfortably.
- Split files by responsibility, not by speculative future layers.
- Remove dead examples, unused helpers, and placeholder code.
- Do not add generated boilerplate unless it is required to run the project.

## Review Checklist

Before finishing any code change, verify:

- The change is related to OpenViking architecture learning.
- Docs were written or updated before code.
- Interfaces are explicit and tested.
- A runnable example exists for each completed feature.
- Tests fail for the intended reason before implementation, then pass.
- The diff does not add broad scaffolding or unrelated functionality.
- The final explanation can describe the architecture in plain language.

## Local Rules And Skills

- Project rule summary: `rules/openviking-mini.md`.
- Review and test skill: `skills/openviking-mini-review/SKILL.md`.
- Tester skill: `skills/openviking-mini-tester/SKILL.md`.
- Example skill: `skills/openviking-mini-example/SKILL.md`.
- Commit skill: `skills/openviking-mini-commit/SKILL.md`.

Use these files when reviewing, testing, or extending the project.
