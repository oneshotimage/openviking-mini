from typing import Protocol

from openviking_mini.models import ToolSpec


class Tool(Protocol):
    @property
    def spec(self) -> ToolSpec:
        ...

    def run(self, input_text: str) -> str:
        ...


class EchoTool:
    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(name="echo", description="Return the input text unchanged.")

    def run(self, input_text: str) -> str:
        return input_text
