from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Task:
    objective: str

    def validate(self) -> Optional[str]:
        if not self.objective.strip():
            return "Task objective must not be blank."
        return None


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str


@dataclass(frozen=True)
class ToolCall:
    tool_name: str
    input_text: str


@dataclass(frozen=True)
class FinalAnswer:
    text: str


@dataclass(frozen=True)
class Event:
    kind: str
    message: str


@dataclass(frozen=True)
class RunResult:
    output: str
    events: tuple[Event, ...]
    succeeded: bool
