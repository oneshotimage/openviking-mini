# Interfaces

This document defines public contracts before implementation.

## VikingURI

Input:

- `raw: str`

Construction:

- `VikingURI.parse(raw: str) -> VikingURI`

Output fields:

- `raw: str`
- `parts: tuple[str, ...]`
- `context_type: ContextType`

Rules:

- URI must start with `viking://`.
- Empty paths normalize to the virtual root.
- Path segments must be non-empty after normalization.
- `.` and `..` segments are rejected.
- Top-level context must be recognized.
- User-scoped paths must include a user id after `user`.

Failure behavior:

- Invalid input raises `VikingURIError` with a concise reason.

## ContextType

Values:

- `ROOT`
- `RESOURCES`
- `USER_MEMORIES`
- `USER_RESOURCES`
- `USER_SKILLS`
- `USER_PEERS`
- `AGENT_MEMORY`

Rules:

- Context type is derived from the normalized `viking://` path.
- User-scoped context must stay separate by user id and subspace.

## Legacy Runtime Contracts

The following contracts are retained only for the existing teaching slice. New feature work should prefer context-database contracts above.

## Task

Input:

- `objective: str`

Rules:

- `objective` must contain non-whitespace text.

## ToolSpec

Input:

- `name: str`
- `description: str`

Rules:

- `name` must be non-empty and unique within a runtime.
- `description` explains the capability for the planner and reader.

## Tool

Contract:

- `spec -> ToolSpec`
- `run(input_text: str) -> str`

Rules:

- `run` receives plain text selected by the planner.
- Tool errors are raised as exceptions and captured by the runtime.

## Planner

Contract:

- `plan(task: Task, tools: Sequence[ToolSpec]) -> Plan`

Plan variants:

- `ToolCall(tool_name: str, input_text: str)`
- `FinalAnswer(text: str)`

Failure behavior:

- A malformed objective becomes `FinalAnswer` with a concise explanation.
- Unknown tools are detected by the runtime because only the runtime owns tool lookup.

## Runtime

Contract:

- `run(task: Task) -> RunResult`

Output:

- `RunResult(output: str, events: tuple[Event, ...], succeeded: bool)`

Rules:

- Record planning and execution events.
- Return `succeeded=False` for missing tools, invalid tasks, and tool exceptions.
- Do not require network access or external services.
