import unittest

from openviking_mini import (
    DeterministicIngestor,
    FirstLineAbstractGenerator,
    FirstLinesOverviewGenerator,
    TokenCountEmbedder,
    Utf8ContentParser,
)


class AdapterTests(unittest.TestCase):
    def test_local_text_adapters_generate_abstract_and_overview(self) -> None:
        content = "OpenViking README\nContext database for agents.\nDetailed notes."

        self.assertEqual(FirstLineAbstractGenerator().generate(content), "OpenViking README")
        self.assertEqual(FirstLinesOverviewGenerator(line_count=2).generate(content), "OpenViking README Context database for agents.")

    def test_token_count_embedder_is_deterministic(self) -> None:
        embedder = TokenCountEmbedder()

        self.assertEqual(embedder.embed("OpenViking context context"), (3.0, 2.0))
        self.assertEqual(embedder.embed("OpenViking context context"), (3.0, 2.0))

    def test_utf8_content_parser_decodes_bytes(self) -> None:
        self.assertEqual(Utf8ContentParser().parse("hello".encode("utf-8")), "hello")

    def test_deterministic_ingestor_uses_injected_text_adapters(self) -> None:
        ingestor = DeterministicIngestor(
            abstract_generator=FixedGenerator("custom abstract"),
            overview_generator=FixedGenerator("custom overview"),
        )

        layer = ingestor.ingest("raw content")

        self.assertEqual(layer.abstract, "custom abstract")
        self.assertEqual(layer.overview, "custom overview")
        self.assertEqual(layer.details, "raw content")


class FixedGenerator:
    def __init__(self, text: str) -> None:
        self._text = text

    def generate(self, content: str) -> str:
        return self._text


if __name__ == "__main__":
    unittest.main()
