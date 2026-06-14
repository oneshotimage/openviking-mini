from openviking_mini import DeterministicIngestor, FirstLineAbstractGenerator, FirstLinesOverviewGenerator, TokenCountEmbedder, Utf8ContentParser


def main() -> None:
    parser = Utf8ContentParser()
    content = parser.parse("OpenViking README\nContext database for agents.".encode("utf-8"))

    ingestor = DeterministicIngestor(
        abstract_generator=FirstLineAbstractGenerator(),
        overview_generator=FirstLinesOverviewGenerator(line_count=2),
    )
    layer = ingestor.ingest(content)

    print(layer.abstract)
    print(layer.overview)
    print(TokenCountEmbedder().embed(layer.overview))


if __name__ == "__main__":
    main()
