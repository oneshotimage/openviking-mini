from openviking_mini import InMemoryVectorIndex, VectorDocument, VikingURI


def main() -> None:
    index = InMemoryVectorIndex(
        embedder=FixedEmbedder(
            {
                "memory query": (1.0, 0.0),
                "memory base": (1.0, 0.0),
                "runtime loop": (0.0, 1.0),
            }
        )
    )
    index.add(VectorDocument(uri=VikingURI.parse("viking://resources/openviking/docs/memory"), text="memory base"))
    index.add(VectorDocument(uri=VikingURI.parse("viking://resources/openviking/docs/runtime"), text="runtime loop"))

    for result in index.search("memory query", top_k=2):
        print(f"{result.score:.1f}:{result.uri}:{result.text}")


class FixedEmbedder:
    def __init__(self, vectors: dict[str, tuple[float, ...]]) -> None:
        self._vectors = vectors

    def embed(self, text: str) -> tuple[float, ...]:
        return self._vectors[text]


if __name__ == "__main__":
    main()
