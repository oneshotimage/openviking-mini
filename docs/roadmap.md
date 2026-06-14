# Roadmap

This roadmap keeps `openviking-mini` aligned with OpenViking's context database / memory base scope.

## Capability Order

1. Filesystem management paradigm
   - Done: `VikingURI` path model.
   - Done: `InMemoryContextStore.add_node`, `ls`, and `read`.
   - Done: `tree`.
   - Next: `grep`.

2. Tiered context loading
   - Add a deterministic ingestion boundary.
   - Add `add_resource` that creates or accepts L0 abstract, L1 overview, and L2 details.
   - Keep model-driven abstract or overview generation behind adapters.

3. Directory recursive retrieval
   - Add query intent analysis.
   - Add deterministic `find` over abstracts and overviews.
   - Add recursive directory refinement.

4. Visualized retrieval trajectory
   - Add trace events for inspected directories and selected nodes.
   - Return retrieval results with trace data.

5. Automatic session management
   - Add explicit session summary input.
   - Add user memory update rules.
   - Add agent experience memory update rules.

## Task Queue

1. Done: Add `tree(uri, max_depth=None)` to `InMemoryContextStore`.
2. Add `grep(pattern, uri)` for deterministic text matching inside a subtree.
3. Add deterministic `add_resource` ingestion with L0/L1/L2 layers.
4. Add model adapter protocols for abstract, overview, embedding, and VLM boundaries without real providers.
5. Add query intent analysis for keyword retrieval conditions.
6. Add `find(query, uri)` using deterministic abstracts and overviews.
7. Add recursive retrieval with directory refinement.
8. Add retrieval trace events and result objects.
9. Add user-scoped access checks for retrieval.
10. Add session memory update contracts.
11. Add user memory updater.
12. Add agent experience memory updater.

Each task must update docs, define interfaces, add failing tests first, implement the smallest behavior, add or update one example, run tests, review the diff, and commit.
