from openviking_mini import ContextLayer, ContextNode, InMemoryContextStore, RecursiveRetriever, VikingURI


def main() -> None:
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

    for result in RecursiveRetriever(store).retrieve("OpenViking context", VikingURI.parse("viking://resources/openviking")):
        print(f"{result.score}:{result.uri}:{','.join(result.matched_terms)}")


if __name__ == "__main__":
    main()
