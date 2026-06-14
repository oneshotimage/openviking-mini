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

## Legacy Teaching Slice

The existing `Task -> Planner -> Tool -> Runtime -> Event` code is a temporary teaching scaffold from the first pass. Do not extend it unless it is migrated toward context indexing, retrieval, or memory update behavior.
