from openviking_mini.models import Event, FinalAnswer, RunResult, Task, ToolCall
from openviking_mini.planner import Planner
from openviking_mini.tools import Tool


class Runtime:
    def __init__(self, planner: Planner, tools: list[Tool]) -> None:
        self._planner = planner
        self._tools = {tool.spec.name: tool for tool in tools}

    def run(self, task: Task) -> RunResult:
        task_error = task.validate()
        if task_error is not None:
            return RunResult(
                output=task_error,
                events=(Event(kind="task_invalid", message=task_error),),
                succeeded=False,
            )

        events: list[Event] = []
        plan = self._planner.plan(task, [tool.spec for tool in self._tools.values()])
        events.append(Event(kind="planned", message=type(plan).__name__))

        if isinstance(plan, FinalAnswer):
            return RunResult(output=plan.text, events=tuple(events), succeeded=False)

        return self._run_tool_call(plan, events)

    def _run_tool_call(self, plan: ToolCall, events: list[Event]) -> RunResult:
        tool = self._tools.get(plan.tool_name)
        if tool is None:
            output = f"Tool not found: {plan.tool_name}"
            events.append(Event(kind="tool_missing", message=output))
            return RunResult(output=output, events=tuple(events), succeeded=False)

        events.append(Event(kind="tool_started", message=plan.tool_name))
        try:
            output = tool.run(plan.input_text)
        except Exception as error:
            message = f"Tool failed: {plan.tool_name}: {error}"
            events.append(Event(kind="tool_failed", message=message))
            return RunResult(output=message, events=tuple(events), succeeded=False)

        events.append(Event(kind="tool_finished", message=plan.tool_name))
        return RunResult(output=output, events=tuple(events), succeeded=True)
