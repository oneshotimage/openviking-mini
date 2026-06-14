---
name: openviking-mini-example
description: Create and maintain openviking-mini examples. Use whenever a feature is completed or changed to add one runnable example under examples/ that demonstrates the public interface, stays minimal, and explains the OpenViking mini architecture behavior without unrelated code.
---

# openviking-mini Example Skill

Use this skill whenever a feature is completed or an existing public interface changes.

## Purpose

Examples show how to use the finished feature through the public interface. They are learning artifacts, not demos, fixtures, or product features.

## Workflow

1. Read `AGENTS.md`.
2. Identify the completed feature and its public interface.
3. Add or update exactly one focused example for that feature unless the feature naturally replaces an older example.
4. Keep the example deterministic and runnable with Python standard library only unless the project already requires more.
5. Run the example command from the repository root and record the result.
6. Ensure tests still pass after the example is added.

## Location And Naming

- Put examples under `examples/`.
- Use descriptive snake_case names, such as `basic_runtime.py`.
- Keep examples short and direct.
- Use `PYTHONPATH=. python3 examples/name.py` until the project has packaging metadata.

## Example Shape

Each example should:

- Import only public objects from `openviking_mini`.
- Construct the smallest meaningful runtime or interface.
- Print stable output that helps a reader see the architecture behavior.
- Avoid private attributes, sleeps, network calls, random values, and decorative formatting.

## Red Flags

- The example uses implementation internals instead of public interfaces.
- The example adds unrelated behavior to make the output look richer.
- The example cannot be run from the repository root.
- The example duplicates test logic without teaching usage.
