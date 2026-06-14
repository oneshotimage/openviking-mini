import math
from dataclasses import dataclass

from openviking_mini.adapters import Embedder
from openviking_mini.retrieval import RetrievalError
from openviking_mini.uri import VikingURI


@dataclass(frozen=True)
class VectorDocument:
    uri: VikingURI
    text: str


@dataclass(frozen=True)
class VectorSearchResult:
    uri: VikingURI
    score: float
    text: str


class InMemoryVectorIndex:
    def __init__(self, embedder: Embedder) -> None:
        self._embedder = embedder
        self._documents: dict[str, VectorDocument] = {}
        self._vectors: dict[str, tuple[float, ...]] = {}

    def add(self, document: VectorDocument) -> None:
        if not document.text.strip():
            raise RetrievalError("vector document text must not be blank.")
        key = str(document.uri)
        self._documents[key] = document
        self._vectors[key] = self._embedder.embed(document.text)

    def search(self, query: str, top_k: int = 5) -> tuple[VectorSearchResult, ...]:
        if not query.strip():
            raise RetrievalError("vector search query must not be blank.")
        if top_k <= 0:
            raise RetrievalError("top_k must be greater than zero.")

        query_vector = self._embedder.embed(query)
        results = []
        for key, vector in self._vectors.items():
            document = self._documents[key]
            results.append(
                VectorSearchResult(
                    uri=document.uri,
                    score=_cosine(query_vector, vector),
                    text=document.text,
                )
            )
        return tuple(sorted(results, key=lambda result: (-result.score, str(result.uri)))[:top_k])


def _cosine(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    if len(left) != len(right):
        raise RetrievalError("vector dimensions must match.")
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    dot = sum(left_value * right_value for left_value, right_value in zip(left, right))
    return dot / (left_norm * right_norm)
