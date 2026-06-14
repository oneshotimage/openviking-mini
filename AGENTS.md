# AGENTS.md

This repository is `openviking-mini`: a learning project for understanding the architecture principles of OpenViking by building the smallest runnable version of its core behavior.

OpenViking is a Context Database / Memory Base for AI agents, not a general-purpose agent runtime. Every feature iteration in this repository must stay inside that scope.

## Mission

- Explain architecture through working code, tests, and short documents.
- Implement only the minimum OpenViking-like context-database core needed to demonstrate the architecture.
- Prefer clarity over completeness. Every module must be easy to read and justify.

## OpenViking Core Capabilities

Every feature must map to at least one of these capabilities. If it does not, do not build it.

1. Filesystem management paradigm
   - Model context as a virtual filesystem under `viking://`.
   - Represent context types such as `resources`, `user` memories, and `agent` skills or memories as structured paths.
   - Prefer deterministic path operations like `ls`, `tree`, `find`, and `grep` over opaque global state.

2. Tiered context loading
   - Store or expose context in layers:
     - `L0 Abstract`: short relevance summary.
     - `L1 Overview`: structure and core information for planning.
     - `L2 Details`: full content loaded only when needed.
   - Do not load full details when an abstract or overview is enough to explain the behavior.

3. Directory recursive retrieval
   - Retrieve by first locating relevant directories, then refining inside those directories.
   - Preserve the idea of hierarchical exploration instead of flat-only search.
   - Keep retrieval deterministic in the mini version unless a later documented interface requires embeddings.

4. Visualized retrieval trajectory
   - Record which directories and nodes were inspected during retrieval.
   - Make retrieval explainable through trace events or path logs.
   - Treat observability as part of the public behavior, not a debug afterthought.

5. Automatic session management and memory self-iteration
   - Summarize session outcomes into explicit user or agent memory updates.
   - Keep user memory and agent experience memory separate.
   - Require tests before adding any automatic memory mutation.

## OpenViking Supporting Boundaries

These boundaries are not optional implementation details. They keep the mini project aligned with OpenViking's context-database shape.

1. Context types
   - Support the distinction between `resources`, `user/{user_id}/memories`, `user/{user_id}/resources`, `user/{user_id}/skills`, `user/{user_id}/peers`, and agent experience memory.
   - Keep user memory, agent memory, resources, skills, and peer context separate in paths and interfaces.
   - Do not collapse all context into a single undifferentiated document store.

2. Native context operations
   - Treat operations such as `add_resource`, `ls`, `tree`, `read`, `find`, and `grep` as core interaction primitives.
   - Implement API-level behavior before adding any CLI or server wrapper.
   - Keep path-based operations deterministic and easy to inspect.

3. Ingestion and semantic processing
   - Adding a resource must have an explicit ingestion boundary.
   - Ingestion should produce or accept L0 abstract, L1 overview, and L2 details.
   - The mini version may use deterministic local processors, but model-driven processing must remain behind interfaces.

4. Model adapters
   - VLM, embedding, abstract generation, and overview generation are adapter boundaries.
   - Do not call external model providers directly from stores, retrievers, or domain models.
   - Prefer local deterministic adapters until a documented testable interface justifies real model integration.

5. Query intent analysis
   - Recursive retrieval begins by turning a query into one or more retrieval conditions.
   - The mini version may implement keyword-based intent analysis first.
   - Keep intent analysis separate from directory traversal and result aggregation.

6. Security and privacy
   - User-scoped context must not leak across users, peers, or private resources.
   - Retrieval must respect context type and path boundaries.
   - Do not add persistence, import, or retrieval behavior that makes private context globally visible.

## Out Of Scope Unless Explicitly Needed By Core Context Management

- General agent orchestration frameworks.
- Chatbot UX.
- Tool-use agents unrelated to context indexing, retrieval, or memory update.
- External model-provider integrations before local deterministic interfaces exist.
- Broad CLI/server implementations before the underlying virtual filesystem and retrieval contracts are tested.

## Hard Boundaries

- Do not copy proprietary OpenViking source code.
- Do not generate unrelated product features, UI pages, integrations, demo fillers, mock SaaS screens, or broad framework scaffolding.
- Do not create large unreadable files or speculative abstractions.
- Do not implement secondary systems before the core architecture is documented and tested.
- Do not add dependencies unless they remove meaningful complexity for the minimal core.
- Do not hide behavior behind magic global state.

## Required Workflow

1. Write or update documentation before implementation.
2. State which OpenViking core capability the feature implements.
3. Define interfaces before implementation details.
4. Write failing tests before production code.
5. Implement the smallest code that makes the tests pass.
6. Refactor only after tests pass and the architecture remains easier to explain.
7. Add or update an example that demonstrates the finished feature.
8. Review the diff against this file before finishing.

## Documentation First

Before adding runtime code, create or update concise docs under `docs/`.

Required docs for core work:

- `docs/architecture.md`: core components, responsibilities, data flow, and why the split exists.
- `docs/interfaces.md`: public interfaces, input/output contracts, error behavior, and extension points.
- `docs/testing.md`: test strategy and how to run tests.

Docs must stay close to the implementation. If code changes an interface or responsibility, update the docs in the same change.

## Architecture Shape

The minimal implementation should separate these context-database concerns:

- URI and path model: parse and validate `viking://` locations.
- Context node model: represent directories, files, and context layers.
- Context store: add, list, read, and search nodes through explicit interfaces.
- Ingestion processor: create or validate L0/L1/L2 context layers before storage.
- Intent analyzer: translate a query into deterministic retrieval conditions.
- Retrieval engine: locate relevant directories and refine results recursively.
- Trace model: record retrieval path, inspected nodes, and selected results.
- Model adapter boundary: isolate VLM, embedding, abstract, and overview generation.
- Session memory updater: turn session summaries into user or agent memories through explicit rules.
- Access boundary: enforce user, peer, private resource, and context type separation.
- Persistence boundary: optional, explicit, and replaceable.

Keep the first version in-process and deterministic unless a test proves a boundary is needed.

The existing `Task -> Planner -> Tool -> Runtime -> Event` slice is only a temporary teaching scaffold. Future iterations must either migrate it toward OpenViking context management or avoid expanding it.

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

- The change maps to at least one OpenViking core capability listed above.
- The change respects the supporting boundaries for context types, native operations, ingestion, model adapters, intent analysis, and security/privacy.
- The change is related to OpenViking context database / memory base architecture learning.
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
