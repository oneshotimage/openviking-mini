# Testing

The project uses Python standard library `unittest` for the first slice.

Run all tests:

```bash
python3 -m unittest discover -s tests
```

Run focused runtime tests:

```bash
python3 -m unittest tests.test_runtime
```

Run the current example:

```bash
PYTHONPATH=. python3 examples/basic_runtime.py
PYTHONPATH=. python3 examples/viking_uri.py
PYTHONPATH=. python3 examples/context_store.py
PYTHONPATH=. python3 examples/context_tree.py
PYTHONPATH=. python3 examples/context_grep.py
PYTHONPATH=. python3 examples/resource_ingestion.py
```

## Strategy

- Test through public interfaces from `openviking_mini`.
- Keep tests deterministic and in-process.
- Cover the successful tool-call path.
- Cover malformed input and missing tool failure paths.
- Avoid tests that depend on network access, time, or external services.
