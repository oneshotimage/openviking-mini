import re
from dataclasses import dataclass
from typing import Protocol

from openviking_mini.uri import VikingURI


class RetrievalError(ValueError):
    """Raised when retrieval preparation or execution violates its contract."""


@dataclass(frozen=True)
class QueryIntent:
    query: str
    terms: tuple[str, ...]


@dataclass(frozen=True)
class FindResult:
    uri: VikingURI
    score: int
    matched_terms: tuple[str, ...]
    abstract: str
    overview: str


class QueryIntentAnalyzer(Protocol):
    def analyze(self, query: str) -> QueryIntent:
        ...


class KeywordIntentAnalyzer:
    _stop_words = {"a", "an", "and", "find", "for", "is", "of", "the", "to", "what"}

    def analyze(self, query: str) -> QueryIntent:
        if not query.strip():
            raise RetrievalError("query must not be blank.")

        terms = []
        seen = set()
        for term in re.findall(r"[A-Za-z0-9]+", query.lower()):
            if term in self._stop_words or term in seen:
                continue
            seen.add(term)
            terms.append(term)

        if not terms:
            raise RetrievalError("query must contain useful terms.")
        return QueryIntent(query=query, terms=tuple(terms))
