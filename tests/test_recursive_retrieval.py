import unittest

from openviking_mini import ContextLayer, ContextNode, InMemoryContextStore, RecursiveRetriever, VikingURI


class RecursiveRetrieverTests(unittest.TestCase):
    def test_refines_through_child_directories(self) -> None:
        store = InMemoryContextStore()
        store.add_node(
            ContextNode(
                uri=VikingURI.parse("viking://resources/openviking/docs/readme"),
                layers=ContextLayer(abstract="OpenViking context", overview="memory base", details="long"),
            )
        )
        store.add_node(
            ContextNode(
                uri=VikingURI.parse("viking://resources/openviking/src/main"),
                layers=ContextLayer(abstract="runtime", overview="context database", details="long"),
            )
        )

        results = RecursiveRetriever(store).retrieve("OpenViking context", VikingURI.parse("viking://resources/openviking"))

        self.assertEqual(
            tuple((str(result.uri), result.score, result.matched_terms) for result in results),
            (
                ("viking://resources/openviking/docs/readme", 2, ("openviking", "context")),
                ("viking://resources/openviking/src/main", 1, ("context",)),
            ),
        )

    def test_respects_recursive_max_depth(self) -> None:
        store = InMemoryContextStore()
        store.add_node(
            ContextNode(
                uri=VikingURI.parse("viking://resources/openviking/docs/readme"),
                layers=ContextLayer(abstract="OpenViking context", overview="memory base", details="long"),
            )
        )

        results = RecursiveRetriever(store).retrieve(
            "OpenViking",
            VikingURI.parse("viking://resources/openviking"),
            max_depth=0,
        )

        self.assertEqual(results, ())


if __name__ == "__main__":
    unittest.main()
