import unittest

from openviking_mini import ContextLayer, ContextNode, ContextStoreError, InMemoryContextStore, VikingURI


class InMemoryContextStoreTests(unittest.TestCase):
    def test_adds_node_and_lists_direct_children(self) -> None:
        store = InMemoryContextStore()
        store.add_node(
            ContextNode(
                uri=VikingURI.parse("viking://resources/openviking/docs/readme"),
                layers=ContextLayer(
                    abstract="OpenViking README",
                    overview="Project overview and quick start",
                    details="OpenViking is a context database for AI agents.",
                ),
            )
        )

        children = store.ls(VikingURI.parse("viking://resources/openviking/docs"))

        self.assertEqual(tuple(str(child) for child in children), ("viking://resources/openviking/docs/readme",))

    def test_lists_only_direct_children_sorted_by_path(self) -> None:
        store = InMemoryContextStore()
        store.add_node(_node("viking://resources/openviking/docs/usage"))
        store.add_node(_node("viking://resources/openviking/src/main"))

        children = store.ls(VikingURI.parse("viking://resources/openviking"))

        self.assertEqual(tuple(str(child) for child in children), ("viking://resources/openviking/docs", "viking://resources/openviking/src"))

    def test_reads_requested_layer_without_loading_details(self) -> None:
        store = InMemoryContextStore()
        store.add_node(_node("viking://user/alice/memories/preferences"))

        self.assertEqual(store.read(VikingURI.parse("viking://user/alice/memories/preferences"), layer="abstract"), "short")
        self.assertEqual(store.read(VikingURI.parse("viking://user/alice/memories/preferences"), layer="overview"), "medium")

    def test_tree_returns_structured_entries_depth_first_by_path(self) -> None:
        store = InMemoryContextStore()
        store.add_node(_node("viking://resources/openviking/docs/readme"))
        store.add_node(_node("viking://resources/openviking/src/main"))

        entries = store.tree(VikingURI.parse("viking://resources/openviking"))

        self.assertEqual(
            tuple((str(entry.uri), entry.depth, entry.is_directory) for entry in entries),
            (
                ("viking://resources/openviking", 0, True),
                ("viking://resources/openviking/docs", 1, True),
                ("viking://resources/openviking/docs/readme", 2, False),
                ("viking://resources/openviking/src", 1, True),
                ("viking://resources/openviking/src/main", 2, False),
            ),
        )

    def test_tree_respects_max_depth(self) -> None:
        store = InMemoryContextStore()
        store.add_node(_node("viking://resources/openviking/docs/readme"))

        entries = store.tree(VikingURI.parse("viking://resources/openviking"), max_depth=1)

        self.assertEqual(
            tuple(str(entry.uri) for entry in entries),
            ("viking://resources/openviking", "viking://resources/openviking/docs"),
        )

    def test_tree_rejects_missing_path(self) -> None:
        store = InMemoryContextStore()

        with self.assertRaisesRegex(ContextStoreError, "not found"):
            store.tree(VikingURI.parse("viking://resources/openviking"))

    def test_grep_searches_subtree_across_layers(self) -> None:
        store = InMemoryContextStore()
        store.add_node(
            ContextNode(
                uri=VikingURI.parse("viking://resources/openviking/docs/readme"),
                layers=ContextLayer(
                    abstract="Context database",
                    overview="OpenViking manages context.",
                    details="Line one\nOpenViking stores memories\nLine three",
                ),
            )
        )
        store.add_node(_node("viking://resources/other/docs/readme"))

        matches = store.grep("openviking", VikingURI.parse("viking://resources/openviking"))

        self.assertEqual(
            tuple((str(match.uri), match.layer, match.line_number, match.line) for match in matches),
            (
                ("viking://resources/openviking/docs/readme", "overview", 1, "OpenViking manages context."),
                ("viking://resources/openviking/docs/readme", "details", 2, "OpenViking stores memories"),
            ),
        )

    def test_grep_can_restrict_to_one_layer(self) -> None:
        store = InMemoryContextStore()
        store.add_node(
            ContextNode(
                uri=VikingURI.parse("viking://resources/openviking/docs/readme"),
                layers=ContextLayer(
                    abstract="OpenViking abstract",
                    overview="OpenViking overview",
                    details="OpenViking details",
                ),
            )
        )

        matches = store.grep("openviking", VikingURI.parse("viking://resources/openviking"), layer="abstract")

        self.assertEqual(tuple(match.layer for match in matches), ("abstract",))

    def test_grep_rejects_missing_path(self) -> None:
        store = InMemoryContextStore()

        with self.assertRaisesRegex(ContextStoreError, "not found"):
            store.grep("openviking", VikingURI.parse("viking://resources/openviking"))

    def test_grep_rejects_blank_pattern(self) -> None:
        store = InMemoryContextStore()

        with self.assertRaisesRegex(ContextStoreError, "pattern"):
            store.grep(" ", VikingURI.parse("viking://"))

    def test_rejects_duplicate_node(self) -> None:
        store = InMemoryContextStore()
        node = _node("viking://resources/openviking/docs/readme")
        store.add_node(node)

        with self.assertRaisesRegex(ContextStoreError, "already exists"):
            store.add_node(node)

    def test_rejects_directory_read(self) -> None:
        store = InMemoryContextStore()
        store.add_node(_node("viking://resources/openviking/docs/readme"))

        with self.assertRaisesRegex(ContextStoreError, "Cannot read directory"):
            store.read(VikingURI.parse("viking://resources/openviking/docs"))

    def test_rejects_missing_path(self) -> None:
        store = InMemoryContextStore()

        with self.assertRaisesRegex(ContextStoreError, "not found"):
            store.read(VikingURI.parse("viking://resources/openviking/missing"))

    def test_rejects_blank_layer_content(self) -> None:
        with self.assertRaisesRegex(ContextStoreError, "abstract"):
            ContextLayer(abstract=" ", overview="medium", details="long")


def _node(raw_uri: str) -> ContextNode:
    return ContextNode(
        uri=VikingURI.parse(raw_uri),
        layers=ContextLayer(abstract="short", overview="medium", details="long"),
    )


if __name__ == "__main__":
    unittest.main()
