# Interfaces

This document defines public contracts before implementation.

## VikingURI

Input:

- `raw: str`

Construction:

- `VikingURI.parse(raw: str) -> VikingURI`

Output fields:

- `raw: str`
- `parts: tuple[str, ...]`
- `context_type: ContextType`

Rules:

- URI must start with `viking://`.
- Empty paths normalize to the virtual root.
- Path segments must be non-empty after normalization.
- `.` and `..` segments are rejected.
- Top-level context must be recognized.
- User-scoped paths must include a user id after `user`.

Failure behavior:

- Invalid input raises `VikingURIError` with a concise reason.

## ContextType

Values:

- `ROOT`
- `RESOURCES`
- `USER_MEMORIES`
- `USER_RESOURCES`
- `USER_SKILLS`
- `USER_PEERS`
- `AGENT_MEMORY`

Rules:

- Context type is derived from the normalized `viking://` path.
- User-scoped context must stay separate by user id and subspace.

## ContextLayer

Input:

- `abstract: str`
- `overview: str`
- `details: str`

Rules:

- Each layer must contain non-whitespace text.
- Layers stay attached to a single context node.
- Store operations may return one layer without loading the others.

## ContextNode

Input:

- `uri: VikingURI`
- `layers: ContextLayer`

Rules:

- A node is addressable only through its validated `VikingURI`.
- The node context type is derived from `uri.context_type`.

## InMemoryContextStore

Contract:

- `add_node(node: ContextNode) -> None`
- `add_resource(uri: VikingURI, content: str, ingestor: ResourceIngestor | None = None) -> ContextNode`
- `ls(uri: VikingURI) -> tuple[VikingURI, ...]`
- `tree(uri: VikingURI, max_depth: int | None = None) -> tuple[TreeEntry, ...]`
- `grep(pattern: str, uri: VikingURI, layer: LayerName | None = None) -> tuple[GrepMatch, ...]`
- `read(uri: VikingURI, layer: LayerName = "details") -> str`

Rules:

- `add_node` creates missing parent directories implicitly.
- `add_resource` requires a `resources`, `user resources`, or `agent memory` URI.
- `add_resource` uses `DeterministicIngestor` by default.
- `add_resource` stores the generated node and returns it.
- `ls` returns direct children only, sorted by path.
- `tree` returns the starting path and descendants sorted by path.
- `tree` depth is relative to the starting URI. The starting path has depth `0`.
- `tree(max_depth=0)` returns only the starting path.
- `grep` searches exact text case-insensitively inside the requested subtree.
- `grep(layer=...)` restricts matching to one layer.
- `grep(layer=None)` searches abstract, overview, and details.
- `grep` returns matches sorted by URI, layer, and line number.
- `read` returns only the requested layer for the exact node.
- `read` on a directory is invalid.
- Missing paths raise `ContextStoreError`.
- Duplicate nodes raise `ContextStoreError`.

Failure behavior:

- Invalid layers, missing nodes, duplicate nodes, and directory reads raise `ContextStoreError` with concise reasons.

## ResourceIngestor

Contract:

- `ingest(content: str) -> ContextLayer`

Rules:

- Ingestion is the only layer-generation boundary.
- Model-backed abstract or overview generation must implement this interface instead of changing the store.

## DeterministicIngestor

Rules:

- `abstract` is the first non-empty line.
- `overview` is the first two non-empty lines joined by a space.
- `details` is the original content stripped of leading and trailing whitespace.
- Blank content raises `ContextStoreError`.

## TreeEntry

Output fields:

- `uri: VikingURI`
- `depth: int`
- `is_directory: bool`

Rules:

- `depth` is relative to the requested tree root.
- Directory entries and file entries both preserve full `viking://` URIs.

## GrepMatch

Output fields:

- `uri: VikingURI`
- `layer: LayerName`
- `line_number: int`
- `line: str`

Rules:

- `line_number` starts at `1`.
- `line` contains the original matching line text.
- Matching is deterministic and does not require embeddings or external services.

## Legacy Runtime Contracts

The following contracts are retained only for the existing teaching slice. New feature work should prefer context-database contracts above.

## Task

Input:

- `objective: str`

Rules:

- `objective` must contain non-whitespace text.

## ToolSpec

Input:

- `name: str`
- `description: str`

Rules:

- `name` must be non-empty and unique within a runtime.
- `description` explains the capability for the planner and reader.

## Tool

Contract:

- `spec -> ToolSpec`
- `run(input_text: str) -> str`

Rules:

- `run` receives plain text selected by the planner.
- Tool errors are raised as exceptions and captured by the runtime.

## Planner

Contract:

- `plan(task: Task, tools: Sequence[ToolSpec]) -> Plan`

Plan variants:

- `ToolCall(tool_name: str, input_text: str)`
- `FinalAnswer(text: str)`

Failure behavior:

- A malformed objective becomes `FinalAnswer` with a concise explanation.
- Unknown tools are detected by the runtime because only the runtime owns tool lookup.

## Runtime

Contract:

- `run(task: Task) -> RunResult`

Output:

- `RunResult(output: str, events: tuple[Event, ...], succeeded: bool)`

Rules:

- Record planning and execution events.
- Return `succeeded=False` for missing tools, invalid tasks, and tool exceptions.
- Do not require network access or external services.
