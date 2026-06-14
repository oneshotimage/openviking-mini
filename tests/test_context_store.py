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
