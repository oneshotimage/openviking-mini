from typing import Protocol


class AbstractGenerator(Protocol):
    def generate(self, content: str) -> str:
        ...


class OverviewGenerator(Protocol):
    def generate(self, content: str) -> str:
        ...


class Embedder(Protocol):
    def embed(self, text: str) -> tuple[float, ...]:
        ...


class ContentParser(Protocol):
    def parse(self, content: bytes) -> str:
        ...


class FirstLineAbstractGenerator:
    def generate(self, content: str) -> str:
        return _non_empty_lines(content)[0]


class FirstLinesOverviewGenerator:
    def __init__(self, line_count: int = 2) -> None:
        if line_count <= 0:
            raise ValueError("line_count must be greater than zero.")
        self._line_count = line_count

    def generate(self, content: str) -> str:
        return " ".join(_non_empty_lines(content)[: self._line_count])


class TokenCountEmbedder:
    def embed(self, text: str) -> tuple[float, ...]:
        tokens = [token for token in text.lower().split() if token]
        return (float(len(tokens)), float(len(set(tokens))))


class Utf8ContentParser:
    def parse(self, content: bytes) -> str:
        return content.decode("utf-8")


def _non_empty_lines(content: str) -> list[str]:
    lines = [line.strip() for line in content.strip().splitlines() if line.strip()]
    if not lines:
        raise ValueError("content must contain at least one non-empty line.")
    return lines
