from dataclasses import dataclass
from typing import Literal, Optional

from openviking_mini.uri import ContextType, VikingURI

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
