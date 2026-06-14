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
- `find(query: str, uri: VikingURI, analyzer: QueryIntentAnalyzer | None = None, max_depth: int | None = None) -> tuple[FindResult, ...]`
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
- `find` searches abstracts and overviews only.
- `find` returns nodes where at least one query term appears.
- `find` scores by number of matched unique terms.
- `find` returns results sorted by score descending, then URI.
- `find(max_depth=...)` limits result depth relative to the requested URI.
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

## Model Adapter Protocols

These protocols define model-backed boundaries without requiring real providers.

### AbstractGenerator

Contract:

- `generate(content: str) -> str`

Rules:

- Returns L0 abstract text.
- Must not mutate context storage.

### OverviewGenerator

Contract:

- `generate(content: str) -> str`

Rules:

- Returns L1 overview text.
- Must not load external resources directly.

### Embedder

Contract:

- `embed(text: str) -> tuple[float, ...]`

Rules:

- Returns deterministic numeric vectors for the same input.
- Real provider integrations must implement this protocol.

### ContentParser

Contract:

- `parse(content: bytes) -> str`

Rules:

- Converts source bytes into text for ingestion.
- VLM-backed parsing must implement this protocol instead of entering the store.

## Local Model Adapters

The mini project provides deterministic local adapters:

- `FirstLineAbstractGenerator`
- `FirstLinesOverviewGenerator`
- `TokenCountEmbedder`
- `Utf8ContentParser`

They are for tests, examples, and local architecture explanation only.

## QueryIntent

Output fields:

- `query: str`
- `terms: tuple[str, ...]`

Rules:

- `terms` are normalized lowercase keywords.
- Duplicate terms are removed while preserving first-seen order.
- Blank queries are invalid.

## QueryIntentAnalyzer

Contract:

- `analyze(query: str) -> QueryIntent`

Rules:

- Analysis only creates retrieval conditions.
- It does not inspect the context store.
- It does not rank or aggregate retrieval results.

## KeywordIntentAnalyzer

Rules:

- Extracts alphanumeric keyword terms.
- Removes a small deterministic stop-word set.
- Raises `RetrievalError` for queries with no useful terms.

## FindResult

Output fields:

- `uri: VikingURI`
- `score: int`
- `matched_terms: tuple[str, ...]`
- `abstract: str`
- `overview: str`

Rules:

- `matched_terms` preserves query-term order.
- `find` does not include L2 details in results.

## RecursiveRetriever

Construction:

- `RecursiveRetriever(store: RecursiveRetrievalStore)`
- `RecursiveRetriever(store: RecursiveRetrievalStore, access_scope: AccessScope | None = None)`

Contract:

- `retrieve(query: str, uri: VikingURI, max_depth: int | None = None) -> tuple[FindResult, ...]`
- `retrieve_with_trace(query: str, uri: VikingURI, max_depth: int | None = None) -> RetrievalRun`

Rules:

- Starts at the requested directory.
- Runs shallow find in each visited directory.
- Descends into child directories until `max_depth` is reached.
- De-duplicates results by URI, preserving the highest score.
- Returns results sorted by score descending, then URI.
- `retrieve_with_trace` includes explainable trajectory events.
- If `access_scope` is provided, starting URI and selected results must be allowed.

## AccessScope

Input:

- `user_id: str | None`
- `allow_public_resources: bool = True`

Rules:

- Public `viking://resources/...` is allowed when `allow_public_resources=True`.
- User paths are allowed only when their user id matches `user_id`.
- Other users' paths are denied.
- Denied starting paths raise `RetrievalError`.
- Denied result paths are skipped.

## RetrievalTraceEvent

Output fields:

- `kind: str`
- `uri: VikingURI`
- `message: str`

Rules:

- `directory_inspected` records each directory visited.
- `result_selected` records each selected context node.

## RetrievalRun

Output fields:

- `results: tuple[FindResult, ...]`
- `trace: tuple[RetrievalTraceEvent, ...]`

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
