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

The first context-database slice implements `VikingURI` parsing and context type detection. It is intentionally small because every future store or retrieval operation depends on this path contract.

## Legacy Teaching Slice

The existing `Task -> Planner -> Tool -> Runtime -> Event` code is a temporary teaching scaffold from the first pass. Do not extend it unless it is migrated toward context indexing, retrieval, or memory update behavior.
