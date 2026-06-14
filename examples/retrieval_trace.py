from openviking_mini import ContextLayer, ContextNode, InMemoryContextStore, RecursiveRetriever, VikingURI


def main() -> None:
    store = InMemoryContextStore()
    store.add_node(
        ContextNode(
            uri=VikingURI.parse("viking://resources/openviking/docs/readme"),
            layers=ContextLayer(abstract="OpenViking context", overview="memory base", details="long"),
        )
    )

    run = RecursiveRetriever(store).retrieve_with_trace("OpenViking", VikingURI.parse("viking://resources/openviking"))
    for event in run.trace:
        print(f"{event.kind}:{event.uri}:{event.message}")


if __name__ == "__main__":
    main()
