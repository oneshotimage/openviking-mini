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
