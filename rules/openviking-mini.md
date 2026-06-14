# openviking-mini Rule

Use this rule for every change in this repository.

## Purpose

Build a minimal runnable OpenViking-inspired core for architecture learning. The project should teach the architecture by combining short docs, explicit interfaces, tests, and small implementation slices.

## Non-Negotiables

- Documentation first.
- Interfaces before implementation.
- Tests before production code.
- Runnable examples for completed features.
- Minimal core behavior only.
- No unrelated examples, UI shells, integrations, or broad scaffolding.
- No large generated files.

## Preferred Slice Order

1. Document the target core concept.
2. Define the interface contract.
3. Write tests around the contract.
4. Implement the smallest runtime behavior.
5. Add or update one example for the feature.
6. Review against `AGENTS.md`.
7. Run the tester skill before considering the change complete.
8. Use the commit skill before staging or committing project changes.

## Review Questions

- Does this change help explain OpenViking-like architecture?
- Can the behavior run locally?
- Is there a small example showing the public interface?
- Can a reader understand the code without reading a huge framework?
- Are failure modes named and tested?
- Did the implementation stay inside the documented boundaries?

## Local Skills

- `skills/openviking-mini-review/SKILL.md`: use for code review.
- `skills/openviking-mini-tester/SKILL.md`: use for test discovery, focused tests, full tests, and test-risk reporting.
- `skills/openviking-mini-example/SKILL.md`: use for creating or updating runnable feature examples.
- `skills/openviking-mini-commit/SKILL.md`: use for clean staging and commit preparation.
