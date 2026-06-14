# openviking-mini Rule

Use this rule for every change in this repository.

## Purpose

Build a minimal runnable OpenViking-inspired context database / memory base for architecture learning. The project should teach the architecture by combining short docs, explicit interfaces, tests, examples, and small implementation slices.

## Core Capability Boundary

Every feature must implement or directly support at least one OpenViking core capability:

- `viking://` virtual filesystem management for resources, user memories, agent skills, and agent memories.
- L0/L1/L2 tiered context loading.
- Directory recursive retrieval.
- Observable retrieval trajectory.
- Automatic session management and memory self-iteration.

Do not build generic agent runtime features unless they directly support one of these context-management capabilities.

## Supporting Boundary Checklist

Check every feature against these boundaries:

- Context types remain distinct: resources, user memory, user resources, user skills, peers, and agent experience memory.
- Native operations are treated as core APIs: `add_resource`, `ls`, `tree`, `read`, `find`, and `grep`.
- Ingestion has an explicit L0/L1/L2 processing boundary.
- Model work stays behind adapters for VLM, embeddings, abstracts, and overviews.
- Query intent analysis is separate from recursive traversal and aggregation.
- Security and privacy preserve user, peer, private resource, and context type boundaries.

## Non-Negotiables

- Documentation first.
- Name the OpenViking core capability before coding.
- Check the supporting boundary checklist before coding.
- Interfaces before implementation.
- Tests before production code.
- Runnable examples for completed features.
- Minimal context-database core behavior only.
- No unrelated examples, UI shells, integrations, or broad scaffolding.
- No large generated files.

## Preferred Slice Order

1. Document the target core concept.
2. Map the feature to one OpenViking core capability.
3. Define the interface contract.
4. Write tests around the contract.
5. Implement the smallest behavior.
6. Add or update one example for the feature.
7. Review against `AGENTS.md`.
8. Run the tester skill before considering the change complete.
9. Use the commit skill before staging or committing project changes.

## Review Questions

- Does this change help explain OpenViking context database architecture?
- Which OpenViking core capability does it implement?
- Which supporting boundary does it touch, and is that boundary still explicit?
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
