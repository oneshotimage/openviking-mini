from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ContextType(Enum):
    ROOT = "root"
    RESOURCES = "resources"
    USER_MEMORIES = "user_memories"
    USER_RESOURCES = "user_resources"
    USER_SKILLS = "user_skills"
    USER_PEERS = "user_peers"
    AGENT_MEMORY = "agent_memory"


class VikingURIError(ValueError):
    """Raised when a viking:// URI violates the path contract."""


@dataclass(frozen=True)
class VikingURI:
    raw: str
    parts: tuple[str, ...]
    context_type: ContextType

    @classmethod
    def parse(cls, raw: str) -> "VikingURI":
        if not raw.startswith("viking://"):
            raise VikingURIError("Viking URI must start with viking://")

        path = raw[len("viking://") :]
        parts = _normalize_parts(path)
        context_type = _context_type_for(parts)
        normalized = "viking://" + "/".join(parts)
        return cls(raw=normalized, parts=parts, context_type=context_type)

    @classmethod
    def from_parts(cls, parts: tuple[str, ...]) -> "VikingURI":
        context_type = _context_type_for(parts)
        normalized = "viking://" + "/".join(parts)
        return cls(raw=normalized, parts=parts, context_type=context_type)

    @property
    def user_id(self) -> Optional[str]:
        if self.parts and self.parts[0] == "user" and len(self.parts) >= 2:
            return self.parts[1]
        return None

    def __str__(self) -> str:
        return self.raw


def _normalize_parts(path: str) -> tuple[str, ...]:
    if path in ("", "/"):
        return ()

    parts = tuple(part for part in path.strip("/").split("/") if part)
    if "." in parts or ".." in parts:
        raise VikingURIError("Path traversal segments are not allowed.")
    return parts


def _context_type_for(parts: tuple[str, ...]) -> ContextType:
    if not parts:
        return ContextType.ROOT

    if parts[0] == "resources":
        return ContextType.RESOURCES

    if parts[0] == "agent":
        if len(parts) >= 2 and parts[1] == "memories":
            return ContextType.AGENT_MEMORY
        raise VikingURIError("Unknown context type under agent.")

    if parts[0] == "user":
        if len(parts) < 2:
            raise VikingURIError("User context path must include a user id.")
        if len(parts) < 3:
            raise VikingURIError("User context path must include a subspace.")
        if parts[2] == "memories":
            return ContextType.USER_MEMORIES
        if parts[2] == "resources":
            return ContextType.USER_RESOURCES
        if parts[2] == "skills":
            return ContextType.USER_SKILLS
        if parts[2] == "peers":
            return ContextType.USER_PEERS
        raise VikingURIError("Unknown context type under user.")

    raise VikingURIError(f"Unknown context type: {parts[0]}")
