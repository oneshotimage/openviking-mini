# Architecture

`openviking-mini` teaches an OpenViking-like context database with the smallest runnable core.

The project direction is the OpenViking context database / memory base:

```text
viking:// URI -> Context Type -> Context Node -> Context Operation -> Trace
```

## Core Components

- `VikingURI`: validates and normalizes `viking://` paths.
- `ContextType`: names the top-level context boundary such as resources or user-scoped memory.
- `Context Node`: represents directories, files, and L0/L1/L2 context layers.
- `Context Store`: owns add, list, tree, read, find, and grep operations.
- `Retrieval Trace`: records which paths were inspected and why.

## Boundaries

The URI and path model is the first boundary. It prevents the system from treating every context item as one flat document bucket.

Context types are part of the path contract. `viking://resources/project` and `viking://user/alice/memories/preference` are not interchangeable.

Native operations such as `ls`, `tree`, `read`, `find`, and `grep` should operate on validated `VikingURI` values, not raw strings.

Security and privacy start at the path model: user-scoped paths must keep their user id visible and explicit.

## Current Slice

Capability:

- Filesystem management paradigm.

Supporting boundaries:

- Context types.
- Native context operations.
- Security and privacy path separation.

The first context-database slice implements `VikingURI` parsing and context type detection. The next slice adds an in-memory context store with native `add_node`, `ls`, `tree`, `read`, and `grep` operations.

`ContextNode` stores content through layers:

- `L0 abstract`: quick relevance check.
- `L1 overview`: structure and key information.
- `L2 details`: full content.

`InMemoryContextStore` keeps context type boundaries by requiring every operation to use a validated `VikingURI`. `tree` returns structured entries instead of formatted text so callers can choose their own display without losing path metadata.

`grep` is deterministic text matching inside one `viking://` subtree. It is not semantic retrieval; it searches stored L0/L1/L2 layers and returns structured matches with URI and layer metadata.

`add_resource` introduces the ingestion boundary. The store accepts raw resource content, delegates layer creation to an ingestor, and stores the resulting `ContextNode`. The first ingestor is deterministic and local; future model-backed abstract or overview generation must live behind the same boundary.

Model adapters are explicit boundaries for future provider-backed processing. The mini implementation includes only deterministic local adapters for abstract generation, overview generation, embedding, and content parsing. Stores and retrievers must depend on these interfaces instead of calling providers directly.

Query intent analysis is separate from retrieval. It converts a raw query into deterministic retrieval conditions that later `find` and recursive retrieval can consume.

`find` is the first retrieval operation. It searches only L0 abstracts and L1 overviews inside a `viking://` subtree using `QueryIntent` terms. It intentionally does not read L2 details.

Recursive retrieval refines by directory. It performs shallow `find` work in the current directory, then descends into child directories and repeats. This keeps directory positioning separate from result aggregation.

Retrieval trace records each inspected directory and each selected result. It is part of the public retrieval output so callers can explain why a context result was returned.

Access scope is checked before retrieval and before result selection. User-scoped retrieval may read public resources and that user's own context, but it must not cross into another user's context.

Session memory starts with explicit contracts. A session summary captures what happened; later updater components decide whether to write user memory or agent experience memory.

User memory updates are derived only from explicit user feedback in a session summary. The updater produces a `MemoryUpdate` first; applying it to a store remains an explicit action.

Agent experience memory updates are derived from tool notes in a session summary. They are written under `viking://agent/memories/...`, keeping agent operational experience separate from user preferences.

Vector retrieval is a separate retrieval boundary. The mini implementation uses an in-memory vector index and an `Embedder` adapter to teach indexing, query embedding, and cosine similarity without external services. The first vector slice indexes L0 abstracts and L1 overviews only.

## Legacy Teaching Slice

The existing `Task -> Planner -> Tool -> Runtime -> Event` code is a temporary teaching scaffold from the first pass. Do not extend it unless it is migrated toward context indexing, retrieval, or memory update behavior.
