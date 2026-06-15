import unittest

from openviking_mini import InMemoryVectorIndex, RetrievalError, VectorDocument, VikingURI


class VectorIndexTests(unittest.TestCase):
    def test_search_ranks_by_cosine_similarity(self) -> None:
        index = InMemoryVectorIndex(embedder=FixedEmbedder({"query": (1.0, 0.0), "alpha": (1.0, 0.0), "beta": (0.0, 1.0)}))
        index.add(VectorDocument(uri=VikingURI.parse("viking://resources/openviking/docs/alpha"), text="alpha"))
        index.add(VectorDocument(uri=VikingURI.parse("viking://resources/openviking/docs/beta"), text="beta"))

        results = index.search("query", top_k=2)

        self.assertEqual(tuple((str(result.uri), result.score) for result in results), (("viking://resources/openviking/docs/alpha", 1.0), ("viking://resources/openviking/docs/beta", 0.0)))

    def test_search_with_trace_records_embedding_scores_and_selection(self) -> None:
        index = InMemoryVectorIndex(embedder=FixedEmbedder({"query": (1.0, 0.0), "alpha": (1.0, 0.0), "beta": (0.0, 1.0)}))
        index.add(VectorDocument(uri=VikingURI.parse("viking://resources/openviking/docs/alpha"), text="alpha"))
        index.add(VectorDocument(uri=VikingURI.parse("viking://resources/openviking/docs/beta"), text="beta"))

        run = index.search_with_trace("query", top_k=1)

        self.assertEqual(tuple(str(result.uri) for result in run.results), ("viking://resources/openviking/docs/alpha",))
        self.assertEqual(
            tuple((event.kind, str(event.uri) if event.uri is not None else "-", event.message) for event in run.trace),
            (
                ("query_embedded", "-", "dimensions=2"),
                ("document_scored", "viking://resources/openviking/docs/alpha", "score=1.000000"),
                ("document_scored", "viking://resources/openviking/docs/beta", "score=0.000000"),
                ("result_selected", "viking://resources/openviking/docs/alpha", "rank=1 score=1.000000"),
            ),
        )

    def test_duplicate_uri_replaces_previous_vector(self) -> None:
        index = InMemoryVectorIndex(embedder=FixedEmbedder({"query": (0.0, 1.0), "old": (1.0, 0.0), "new": (0.0, 1.0)}))
        uri = VikingURI.parse("viking://resources/openviking/docs/readme")
        index.add(VectorDocument(uri=uri, text="old"))
        index.add(VectorDocument(uri=uri, text="new"))

        results = index.search("query")

        self.assertEqual(tuple(result.text for result in results), ("new",))

    def test_rejects_blank_query(self) -> None:
        index = InMemoryVectorIndex(embedder=FixedEmbedder({}))

        with self.assertRaisesRegex(RetrievalError, "query"):
            index.search(" ")

    def test_rejects_non_positive_top_k(self) -> None:
        index = InMemoryVectorIndex(embedder=FixedEmbedder({}))

        with self.assertRaisesRegex(RetrievalError, "top_k"):
            index.search("query", top_k=0)

    def test_search_with_trace_rejects_blank_query(self) -> None:
        index = InMemoryVectorIndex(embedder=FixedEmbedder({}))

        with self.assertRaisesRegex(RetrievalError, "query"):
            index.search_with_trace(" ")


class FixedEmbedder:
    def __init__(self, vectors: dict[str, tuple[float, ...]]) -> None:
        self._vectors = vectors

    def embed(self, text: str) -> tuple[float, ...]:
        return self._vectors.get(text, (0.0, 0.0))


if __name__ == "__main__":
    unittest.main()
