from dataclasses import dataclass

from openviking_mini.context_store import ContextLayer
from openviking_mini.uri import ContextType, VikingURI


class MemoryUpdateError(ValueError):
    """Raised when a session memory contract is invalid."""


@dataclass(frozen=True)
class SessionSummary:
    user_id: str
    objective: str
    outcome: str
    user_feedback: str = ""
    tool_notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text("user_id", self.user_id)
        _require_text("objective", self.objective)
        _require_text("outcome", self.outcome)


@dataclass(frozen=True)
class MemoryUpdate:
    uri: VikingURI
    layers: ContextLayer
    reason: str

    def __post_init__(self) -> None:
        if self.uri.context_type not in (ContextType.USER_MEMORIES, ContextType.AGENT_MEMORY):
            raise MemoryUpdateError(f"Memory update URI must target memory context: {self.uri}")
        _require_text("reason", self.reason)


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise MemoryUpdateError(f"{name} must not be blank.")
