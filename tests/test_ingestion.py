import unittest

from openviking_mini import ContextLayer, ContextStoreError, DeterministicIngestor, InMemoryContextStore, VikingURI


class IngestionTests(unittest.TestCase):
    def test_add_resource_builds_layers_and_stores_node(self) -> None:
        store = InMemoryContextStore()

        node = store.add_resource(
            VikingURI.parse("viking://resources/openviking/docs/readme"),
            "OpenViking README\nContext database for agents.\nMore details.",
        )

        self.assertEqual(node.layers.abstract, "OpenViking README")
        self.assertEqual(node.layers.overview, "OpenViking README Context database for agents.")
        self.assertEqual(store.read(VikingURI.parse("viking://resources/openviking/docs/readme"), layer="details"), "OpenViking README\nContext database for agents.\nMore details.")

    def test_add_resource_rejects_non_resource_memory_path(self) -> None:
        store = InMemoryContextStore()

        with self.assertRaisesRegex(ContextStoreError, "resource ingestion"):
            store.add_resource(VikingURI.parse("viking://user/alice/memories/preferences"), "prefers concise docs")

    def test_add_resource_accepts_user_resource_path(self) -> None:
        store = InMemoryContextStore()

        node = store.add_resource(VikingURI.parse("viking://user/alice/resources/private_project/readme"), "Private project")

        self.assertEqual(node.uri.context_type.value, "user_resources")

    def test_add_resource_accepts_custom_ingestor_boundary(self) -> None:
        store = InMemoryContextStore()

        node = store.add_resource(
            VikingURI.parse("viking://resources/openviking/docs/readme"),
            "raw content",
            ingestor=FixedIngestor(),
        )

        self.assertEqual(node.layers.abstract, "fixed abstract")

    def test_deterministic_ingestor_rejects_blank_content(self) -> None:
        with self.assertRaisesRegex(ContextStoreError, "content"):
            DeterministicIngestor().ingest(" ")


class FixedIngestor:
    def ingest(self, content: str) -> ContextLayer:
        return ContextLayer(abstract="fixed abstract", overview="fixed overview", details=content)


if __name__ == "__main__":
    unittest.main()
