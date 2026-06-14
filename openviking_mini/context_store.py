from dataclasses import dataclass
from typing import Literal, Optional, Protocol, get_args

from openviking_mini.uri import ContextType, VikingURI
from openviking_mini.retrieval import FindResult, QueryIntentAnalyzer

LayerName = Literal["abstract", "overview", "details"]


class ContextStoreError(ValueError):
    """Raised when a context store operation violates the store contract."""


@dataclass(frozen=True)
class ContextLayer:
    abstract: str
    overview: str
    details: str

    def __post_init__(self) -> None:
        for name, value in (
            ("abstract", self.abstract),
            ("overview", self.overview),
            ("details", self.details),
        ):
            if not value.strip():
                raise ContextStoreError(f"Context layer {name} must not be blank.")

    def read(self, layer: LayerName) -> str:
        if layer == "abstract":
            return self.abstract
        if layer == "overview":
            return self.overview
        if layer == "details":
            return self.details
        raise ContextStoreError(f"Unknown context layer: {layer}")


class ResourceIngestor(Protocol):
    def ingest(self, content: str) -> ContextLayer:
        ...


@dataclass(frozen=True)
class ContextNode:
    uri: VikingURI
    layers: ContextLayer

    @property
    def context_type(self) -> ContextType:
        return self.uri.context_type


@dataclass(frozen=True)
class TreeEntry:
    uri: VikingURI
    depth: int
    is_directory: bool


@dataclass(frozen=True)
class GrepMatch:
    uri: VikingURI
    layer: LayerName
    line_number: int
    line: str


class InMemoryContextStore:
    def __init__(self) -> None:
        self._nodes: dict[tuple[str, ...], ContextNode] = {}
        self._directories: set[tuple[str, ...]] = {()}

    def add_node(self, node: ContextNode) -> None:
        key = node.uri.parts
        if key in self._nodes:
            raise ContextStoreError(f"Context node already exists: {node.uri}")
        if not key:
            raise ContextStoreError("Cannot add a node at viking:// root.")

        self._add_parent_directories(key)
        self._nodes[key] = node

    def add_resource(self, uri: VikingURI, content: str, ingestor: Optional[ResourceIngestor] = None) -> ContextNode:
        if uri.context_type not in (
            ContextType.RESOURCES,
            ContextType.USER_RESOURCES,
            ContextType.AGENT_MEMORY,
        ):
            raise ContextStoreError(f"URI is not valid for resource ingestion: {uri}")

        from openviking_mini.ingestion import DeterministicIngestor

        active_ingestor = ingestor if ingestor is not None else DeterministicIngestor()
        layers = active_ingestor.ingest(content)
        node = ContextNode(uri=uri, layers=layers)
        self.add_node(node)
        return node

    def ls(self, uri: VikingURI) -> tuple[VikingURI, ...]:
        key = uri.parts
        if key not in self._directories:
            raise ContextStoreError(f"Directory not found: {uri}")

        child_parts = set()
        for directory in self._directories:
            if len(directory) == len(key) + 1 and directory[: len(key)] == key:
                child_parts.add(directory)
        for node_key in self._nodes:
            if len(node_key) == len(key) + 1 and node_key[: len(key)] == key:
                child_parts.add(node_key)

        return tuple(VikingURI.from_parts(parts) for parts in sorted(child_parts))

    def tree(self, uri: VikingURI, max_depth: Optional[int] = None) -> tuple[TreeEntry, ...]:
        key = uri.parts
        if key not in self._directories and key not in self._nodes:
            raise ContextStoreError(f"Path not found: {uri}")
        if max_depth is not None and max_depth < 0:
            raise ContextStoreError("max_depth must be zero or greater.")

        entries = []
        for parts in self._tree_parts(key, max_depth):
            entries.append(
                TreeEntry(
                    uri=VikingURI.from_parts(parts),
                    depth=len(parts) - len(key),
                    is_directory=parts in self._directories,
                )
            )
        return tuple(entries)

    def grep(self, pattern: str, uri: VikingURI, layer: Optional[LayerName] = None) -> tuple[GrepMatch, ...]:
        key = uri.parts
        if not pattern.strip():
            raise ContextStoreError("grep pattern must not be blank.")
        if key not in self._directories and key not in self._nodes:
            raise ContextStoreError(f"Path not found: {uri}")

        layers = (layer,) if layer is not None else get_args(LayerName)
        matches = []
        lowered_pattern = pattern.lower()
        for node_key in sorted(self._nodes):
            if node_key[: len(key)] != key:
                continue
            node = self._nodes[node_key]
            for layer_name in layers:
                text = node.layers.read(layer_name)
                for line_number, line in enumerate(text.splitlines(), start=1):
                    if lowered_pattern in line.lower():
                        matches.append(
                            GrepMatch(
                                uri=node.uri,
                                layer=layer_name,
                                line_number=line_number,
                                line=line,
                            )
                        )
        return tuple(matches)

    def find(
        self,
        query: str,
        uri: VikingURI,
        analyzer: Optional[QueryIntentAnalyzer] = None,
    ) -> tuple[FindResult, ...]:
        key = uri.parts
        if key not in self._directories and key not in self._nodes:
            raise ContextStoreError(f"Path not found: {uri}")

        from openviking_mini.retrieval import KeywordIntentAnalyzer

        active_analyzer = analyzer if analyzer is not None else KeywordIntentAnalyzer()
        intent = active_analyzer.analyze(query)
        results = []
        for node_key in sorted(self._nodes):
            if node_key[: len(key)] != key:
                continue
            node = self._nodes[node_key]
            searchable = f"{node.layers.abstract}\n{node.layers.overview}".lower()
            matched_terms = tuple(term for term in intent.terms if term in searchable)
            if not matched_terms:
                continue
            results.append(
                FindResult(
                    uri=node.uri,
                    score=len(matched_terms),
                    matched_terms=matched_terms,
                    abstract=node.layers.abstract,
                    overview=node.layers.overview,
                )
            )
        return tuple(sorted(results, key=lambda result: (-result.score, str(result.uri))))

    def read(self, uri: VikingURI, layer: LayerName = "details") -> str:
        key = uri.parts
        if key in self._directories and key not in self._nodes:
            raise ContextStoreError(f"Cannot read directory: {uri}")

        node = self._nodes.get(key)
        if node is None:
            raise ContextStoreError(f"Context node not found: {uri}")
        return node.layers.read(layer)

    def _add_parent_directories(self, key: tuple[str, ...]) -> None:
        for index in range(len(key)):
            self._directories.add(key[:index])

    def _tree_parts(self, key: tuple[str, ...], max_depth: Optional[int]) -> tuple[tuple[str, ...], ...]:
        all_parts = self._directories | set(self._nodes)
        subtree = []
        for parts in all_parts:
            if parts[: len(key)] != key:
                continue
            depth = len(parts) - len(key)
            if max_depth is not None and depth > max_depth:
                continue
            subtree.append(parts)
        return tuple(sorted(subtree))
