# Roadmap

This roadmap keeps `openviking-mini` aligned with OpenViking's context database / memory base scope.

## Capability Order

1. Filesystem management paradigm
   - Done: `VikingURI` path model.
   - Done: `InMemoryContextStore.add_node`, `ls`, and `read`.
   - Done: `tree`.
   - Done: `grep`.

2. Tiered context loading
   - Done: Add a deterministic ingestion boundary.
   - Done: Add `add_resource` that creates or accepts L0 abstract, L1 overview, and L2 details.
   - Done: Keep model-driven abstract or overview generation behind adapters.

3. Directory recursive retrieval
   - Done: Add query intent analysis.
   - Done: Add deterministic `find` over abstracts and overviews.
   - Done: Add recursive directory refinement.

4. Visualized retrieval trajectory
   - Done: Add trace events for inspected directories and selected nodes.
   - Done: Return retrieval results with trace data.

5. Automatic session management
   - Done: Add explicit session summary input.
   - Done: Add user memory update rules.
   - Done: Add agent experience memory update rules.

## Task Queue

1. Done: Add `tree(uri, max_depth=None)` to `InMemoryContextStore`.
2. Done: Add `grep(pattern, uri)` for deterministic text matching inside a subtree.
3. Done: Add deterministic `add_resource` ingestion with L0/L1/L2 layers.
4. Done: Add model adapter protocols for abstract, overview, embedding, and VLM boundaries without real providers.
5. Done: Add query intent analysis for keyword retrieval conditions.
6. Done: Add `find(query, uri)` using deterministic abstracts and overviews.
7. Done: Add recursive retrieval with directory refinement.
8. Done: Add retrieval trace events and result objects.
9. Done: Add user-scoped access checks for retrieval.
10. Done: Add session memory update contracts.
11. Done: Add user memory updater.
12. Done: Add agent experience memory updater.

All planned roadmap tasks are complete. Future work should start by adding a new roadmap item that maps to an OpenViking core capability.

## Vector Retrieval Learning Track

1. Add `InMemoryVectorIndex` with cosine similarity over L0/L1 text.
2. Add vector search trace events.
3. Integrate vector search into recursive retrieval as a directory-positioning signal.
4. Add an embedding adapter test double that can emulate semantic closeness beyond exact keywords.
5. Add access-scope checks to vector search.

Each task must update docs, define interfaces, add failing tests first, implement the smallest behavior, add or update one example, run tests, review the diff, and commit.
