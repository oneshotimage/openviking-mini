# Architecture

`openviking-mini` teaches an OpenViking-like agent runtime with the smallest runnable core.

The first slice models one deterministic loop:

```text
Task -> Planner -> ToolCall -> Tool -> Event Log -> RunResult
```

## Components

- `Task`: user intent for one run.
- `Planner`: turns a task and available tools into either a `ToolCall` or a final answer.
- `Tool`: executes one explicit capability behind a stable interface.
- `Runtime`: coordinates planning, tool lookup, execution, and event recording.
- `Event`: records what happened without coupling the domain model to printing or storage.

## Boundaries

Domain objects are plain data and do not execute tools.

The planner decides what should happen next but does not call tools.

The runtime owns execution. It is the only layer that looks up a tool by name and records the result.

Tools are replaceable. The first implementation includes an in-memory `EchoTool` only to prove the boundary.

## First Slice

The first planner accepts commands in this form:

```text
tool_name: input text
```

If the tool exists, the runtime executes it and returns the tool output. If the command is malformed or the tool is missing, the runtime returns a clear failure result.

This is intentionally small: it demonstrates the architecture loop without adding networking, persistence, model calls, or unrelated UI.
