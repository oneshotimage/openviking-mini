# Examples

Examples live under `examples/` and demonstrate public interfaces.

## Basic Runtime

Run:

```bash
PYTHONPATH=. python3 examples/basic_runtime.py
```

Expected output:

```text
hello architecture
planned,tool_started,tool_finished
```

This example shows the first core loop: a `Task` is planned into a tool call, executed by the `Runtime`, and recorded as events.

## Viking URI

Run:

```bash
PYTHONPATH=. python3 examples/viking_uri.py
```

Expected output:

```text
viking://resources/openviking/docs -> resources
viking://user/alice/memories/preferences -> user_memories
viking://user/alice/skills/search_code -> user_skills
```

This example shows how the public `VikingURI` interface keeps context types visible in the path model.

## Context Store

Run:

```bash
PYTHONPATH=. python3 examples/context_store.py
```

Expected output:

```text
viking://resources/openviking/docs/readme
OpenViking README
```

This example shows how `InMemoryContextStore` adds a layered context node, lists direct children, and reads only the requested layer.

## Context Tree

Run:

```bash
PYTHONPATH=. python3 examples/context_tree.py
```

Expected output:

```text
0:dir:viking://resources/openviking
1:dir:viking://resources/openviking/docs
2:file:viking://resources/openviking/docs/readme
1:dir:viking://resources/openviking/src
2:file:viking://resources/openviking/src/main
```

This example shows how `tree` returns structured entries with relative depth and directory/file metadata.

## Context Grep

Run:

```bash
PYTHONPATH=. python3 examples/context_grep.py
```

Expected output:

```text
viking://resources/openviking/docs/readme:abstract:1:OpenViking README
viking://resources/openviking/docs/readme:overview:1:OpenViking manages context.
viking://resources/openviking/docs/readme:details:2:OpenViking stores memories
```

This example shows deterministic text matching inside one `viking://` subtree.

## Resource Ingestion

Run:

```bash
PYTHONPATH=. python3 examples/resource_ingestion.py
```

Expected output:

```text
OpenViking README
OpenViking README Context database for AI agents.
OpenViking README
Context database for AI agents.
Detailed project notes.
```

This example shows deterministic L0/L1/L2 layer creation through `add_resource`.

## Model Adapters

Run:

```bash
PYTHONPATH=. python3 examples/model_adapters.py
```

Expected output:

```text
OpenViking README
OpenViking README Context database for agents.
(6.0, 6.0)
```

This example shows local adapter boundaries for parsing, abstract generation, overview generation, and embedding.

## Query Intent

Run:

```bash
PYTHONPATH=. python3 examples/query_intent.py
```

Expected output:

```text
Find the OpenViking context memory
openviking,context,memory
```

This example shows deterministic query intent analysis before retrieval.

## Context Find

Run:

```bash
PYTHONPATH=. python3 examples/context_find.py
```

Expected output:

```text
2:viking://resources/openviking/docs/readme:openviking,memory
```

This example shows deterministic retrieval over L0 abstracts and L1 overviews.

## Recursive Retrieval

Run:

```bash
PYTHONPATH=. python3 examples/recursive_retrieval.py
```

Expected output:

```text
2:viking://resources/openviking/docs/readme:openviking,context
1:viking://resources/openviking/src/main:context
```

This example shows directory-by-directory refinement before trace events are added.

## Retrieval Trace

Run:

```bash
PYTHONPATH=. python3 examples/retrieval_trace.py
```

Expected output:

```text
directory_inspected:viking://resources/openviking:depth=0
directory_inspected:viking://resources/openviking/docs:depth=1
result_selected:viking://resources/openviking/docs/readme:score=1
```

This example shows the observable retrieval trajectory.

## Access Scope

Run:

```bash
PYTHONPATH=. python3 examples/access_scope.py
```

Expected output:

```text
viking://user/alice/resources/private/readme
```

This example shows user-scoped retrieval access.

## Memory Contracts

Run:

```bash
PYTHONPATH=. python3 examples/memory_contracts.py
```

Expected output:

```text
alice
viking://user/alice/memories/preferences/concise
User feedback indicated a concise style preference.
```

This example shows session memory update contracts without applying memory mutation.

## User Memory Updater

Run:

```bash
PYTHONPATH=. python3 examples/user_memory_updater.py
```

Expected output:

```text
viking://user/alice/memories/session/answer-architecture-question
Prefer concise answers.
```

This example shows explicit user memory update application from session feedback.

## Agent Experience Updater

Run:

```bash
PYTHONPATH=. python3 examples/agent_experience_updater.py
```

Expected output:

```text
viking://agent/memories/session/answer-architecture-question
Use grep before find.
Keep retrieval scoped.
```

This example shows agent experience memory update application from tool notes.
