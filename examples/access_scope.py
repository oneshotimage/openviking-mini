from openviking_mini import AccessScope, ContextLayer, ContextNode, InMemoryContextStore, RecursiveRetriever, VikingURI


def main() -> None:
    store = InMemoryContextStore()
    store.add_node(
        ContextNode(
            uri=VikingURI.parse("viking://user/alice/resources/private/readme"),
            layers=ContextLayer(abstract="private", overview="alice private context", details="long"),
        )
    )

    results = RecursiveRetriever(store, access_scope=AccessScope(user_id="alice")).retrieve(
        "private",
        VikingURI.parse("viking://user/alice/resources"),
    )

    for result in results:
        print(result.uri)


if __name__ == "__main__":
    main()
