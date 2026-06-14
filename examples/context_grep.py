from openviking_mini import ContextLayer, ContextNode, InMemoryContextStore, VikingURI


def main() -> None:
    store = InMemoryContextStore()
    store.add_node(
        ContextNode(
            uri=VikingURI.parse("viking://resources/openviking/docs/readme"),
            layers=ContextLayer(
                abstract="OpenViking README",
                overview="OpenViking manages context.",
                details="Line one\nOpenViking stores memories\nLine three",
            ),
        )
    )

    for match in store.grep("openviking", VikingURI.parse("viking://resources/openviking")):
        print(f"{match.uri}:{match.layer}:{match.line_number}:{match.line}")


if __name__ == "__main__":
    main()
