import re
from dataclasses import dataclass
from typing import Optional, Protocol

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


@dataclass(frozen=True)
class RetrievalTraceEvent:
    kind: str
    uri: VikingURI
    message: str


@dataclass(frozen=True)
class RetrievalRun:
    results: tuple[FindResult, ...]
    trace: tuple[RetrievalTraceEvent, ...]


@dataclass(frozen=True)
class AccessScope:
    user_id: Optional[str] = None
    allow_public_resources: bool = True

    def allows(self, uri: VikingURI) -> bool:
        if uri.context_type.value == "resources":
            return self.allow_public_resources
        if uri.parts and uri.parts[0] == "user":
            return uri.user_id == self.user_id and not _is_peer_path(uri)
        return self.user_id is None


class QueryIntentAnalyzer(Protocol):
    def analyze(self, query: str) -> QueryIntent:
        ...


class RecursiveRetrievalStore(Protocol):
    def tree(self, uri: VikingURI, max_depth: Optional[int] = None) -> tuple[object, ...]:
        ...

    def find(
        self,
        query: str,
        uri: VikingURI,
        analyzer: Optional[QueryIntentAnalyzer] = None,
        max_depth: Optional[int] = None,
    ) -> tuple[FindResult, ...]:
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


class RecursiveRetriever:
    def __init__(
        self,
        store: RecursiveRetrievalStore,
        analyzer: Optional[QueryIntentAnalyzer] = None,
        access_scope: Optional[AccessScope] = None,
    ) -> None:
        self._store = store
        self._analyzer = analyzer or KeywordIntentAnalyzer()
        self._access_scope = access_scope

    def retrieve(self, query: str, uri: VikingURI, max_depth: Optional[int] = None) -> tuple[FindResult, ...]:
        return self.retrieve_with_trace(query, uri, max_depth=max_depth).results

    def retrieve_with_trace(self, query: str, uri: VikingURI, max_depth: Optional[int] = None) -> RetrievalRun:
        if self._access_scope is not None and not self._access_scope.allows(uri):
            raise RetrievalError(f"Access denied for retrieval root: {uri}")

        results_by_uri: dict[str, FindResult] = {}
        trace = []
        for entry in self._store.tree(uri, max_depth=max_depth):
            if not entry.is_directory:
                continue
            if self._access_scope is not None and not self._access_scope.allows(entry.uri):
                continue
            trace.append(RetrievalTraceEvent(kind="directory_inspected", uri=entry.uri, message=f"depth={entry.depth}"))
            for result in self._store.find(query, entry.uri, analyzer=self._analyzer, max_depth=1):
                if self._access_scope is not None and not self._access_scope.allows(result.uri):
                    continue
                key = str(result.uri)
                existing = results_by_uri.get(key)
                if existing is None or result.score > existing.score:
                    results_by_uri[key] = result

        results = tuple(sorted(results_by_uri.values(), key=lambda result: (-result.score, str(result.uri))))
        for result in results:
            trace.append(RetrievalTraceEvent(kind="result_selected", uri=result.uri, message=f"score={result.score}"))
        return RetrievalRun(results=results, trace=tuple(trace))


def _is_peer_path(uri: VikingURI) -> bool:
    return len(uri.parts) >= 3 and uri.parts[0] == "user" and uri.parts[2] == "peers"
