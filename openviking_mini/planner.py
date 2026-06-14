from collections.abc import Sequence
from typing import Protocol, Union

from openviking_mini.models import FinalAnswer, Task, ToolCall, ToolSpec

Plan = Union[ToolCall, FinalAnswer]


class Planner(Protocol):
    def plan(self, task: Task, tools: Sequence[ToolSpec]) -> Plan:
        ...


class PrefixPlanner:
    def plan(self, task: Task, tools: Sequence[ToolSpec]) -> Plan:
        if ":" not in task.objective:
            return FinalAnswer("Expected objective format: tool_name: input text")

        tool_name, input_text = task.objective.split(":", 1)
        tool_name = tool_name.strip()
        input_text = input_text.strip()

        if not tool_name or not input_text:
            return FinalAnswer("Expected objective format: tool_name: input text")

        return ToolCall(tool_name=tool_name, input_text=input_text)
