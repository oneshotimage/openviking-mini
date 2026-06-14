from openviking_mini import ContextLayer, ContextNode, InMemoryContextStore, VikingURI


def main() -> None:
    store = InMemoryContextStore()
    store.add_node(
        ContextNode(
            uri=VikingURI.parse("viking://resources/openviking/docs/readme"),
            layers=ContextLayer(
                abstract="OpenViking README",
                overview="Context database overview",
                details="OpenViking manages resources, memories, and skills with viking:// paths.",
            ),
        )
    )

    for child in store.ls(VikingURI.parse("viking://resources/openviking/docs")):
        print(child)

    print(store.read(VikingURI.parse("viking://resources/openviking/docs/readme"), layer="abstract"))


if __name__ == "__main__":
    main()
