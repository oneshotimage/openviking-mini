from openviking_mini import VikingURI


def main() -> None:
    for raw in (
        "viking://resources/openviking/docs",
        "viking://user/alice/memories/preferences",
        "viking://user/alice/skills/search_code",
    ):
        uri = VikingURI.parse(raw)
        print(f"{uri} -> {uri.context_type.value}")


if __name__ == "__main__":
    main()
