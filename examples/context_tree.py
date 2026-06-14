from openviking_mini import ContextLayer, ContextNode, InMemoryContextStore, VikingURI


def main() -> None:
    store = InMemoryContextStore()
    for raw_uri in (
        "viking://resources/openviking/docs/readme",
        "viking://resources/openviking/src/main",
    ):
        store.add_node(
            ContextNode(
                uri=VikingURI.parse(raw_uri),
                layers=ContextLayer(abstract="short", overview="medium", details="long"),
            )
        )

    for entry in store.tree(VikingURI.parse("viking://resources/openviking")):
        kind = "dir" if entry.is_directory else "file"
        print(f"{entry.depth}:{kind}:{entry.uri}")


if __name__ == "__main__":
    main()
