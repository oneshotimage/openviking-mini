from openviking_mini import InMemoryVectorIndex, VectorDocument, VikingURI


class FixedEmbedder:
    def __init__(self, vectors: dict[str, tuple[float, ...]]) -> None:
        self._vectors = vectors

    def embed(self, text: str) -> tuple[float, ...]:
        return self._vectors[text]


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

    run = index.search_with_trace("memory query", top_k=1)

    for event in run.trace:
        uri = str(event.uri) if event.uri is not None else "-"
        print(f"{event.kind}:{uri}:{event.message}")


if __name__ == "__main__":
    main()
