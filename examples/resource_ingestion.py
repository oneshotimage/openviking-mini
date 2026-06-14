from openviking_mini import InMemoryContextStore, VikingURI


def main() -> None:
    store = InMemoryContextStore()
    uri = VikingURI.parse("viking://resources/openviking/docs/readme")
    store.add_resource(
        uri,
        "OpenViking README\nContext database for AI agents.\nDetailed project notes.",
    )

    print(store.read(uri, layer="abstract"))
    print(store.read(uri, layer="overview"))
    print(store.read(uri, layer="details"))


if __name__ == "__main__":
    main()
