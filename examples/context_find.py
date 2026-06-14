from openviking_mini import ContextLayer, ContextNode, InMemoryContextStore, VikingURI


def main() -> None:
    store = InMemoryContextStore()
    store.add_node(
        ContextNode(
            uri=VikingURI.parse("viking://resources/openviking/docs/readme"),
            layers=ContextLayer(
                abstract="OpenViking context database",
                overview="Memory base for agents",
                details="Full details stay out of find results.",
            ),
        )
    )

    for result in store.find("OpenViking memory", VikingURI.parse("viking://resources/openviking")):
        print(f"{result.score}:{result.uri}:{','.join(result.matched_terms)}")


if __name__ == "__main__":
    main()
