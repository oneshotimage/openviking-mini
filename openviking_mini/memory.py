from dataclasses import dataclass
import re
from typing import Optional

from openviking_mini.context_store import ContextLayer, ContextNode, InMemoryContextStore
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


class UserMemoryUpdater:
    def build_update(self, summary: SessionSummary) -> Optional[MemoryUpdate]:
        feedback = summary.user_feedback.strip()
        if not feedback:
            return None

        uri = VikingURI.parse(f"viking://user/{summary.user_id}/memories/session/{_slug(summary.objective)}")
        layers = ContextLayer(
            abstract=feedback,
            overview=f"User feedback for session objective: {summary.objective}",
            details=feedback,
        )
        return MemoryUpdate(uri=uri, layers=layers, reason="Session user feedback provided.")

    def apply(self, store: InMemoryContextStore, summary: SessionSummary) -> Optional[MemoryUpdate]:
        update = self.build_update(summary)
        if update is None:
            return None
        store.add_node(ContextNode(uri=update.uri, layers=update.layers))
        return update


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise MemoryUpdateError(f"{name} must not be blank.")


def _slug(text: str) -> str:
    parts = re.findall(r"[a-z0-9]+", text.lower())
    return "-".join(parts[:6]) or "session"
