# Examples

Examples live under `examples/` and demonstrate public interfaces.

## Basic Runtime

Run:

```bash
PYTHONPATH=. python3 examples/basic_runtime.py
```

Expected output:

```text
hello architecture
planned,tool_started,tool_finished
```

This example shows the first core loop: a `Task` is planned into a tool call, executed by the `Runtime`, and recorded as events.
