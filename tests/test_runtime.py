import unittest

from openviking_mini import EchoTool, PrefixPlanner, Runtime, Task


class RuntimeTests(unittest.TestCase):
    def test_runs_tool_selected_by_prefix_planner(self) -> None:
        runtime = Runtime(planner=PrefixPlanner(), tools=[EchoTool()])

        result = runtime.run(Task("echo: hello architecture"))

        self.assertTrue(result.succeeded)
        self.assertEqual(result.output, "hello architecture")
        self.assertEqual([event.kind for event in result.events], ["planned", "tool_started", "tool_finished"])

    def test_malformed_objective_returns_failure_without_tool_execution(self) -> None:
        runtime = Runtime(planner=PrefixPlanner(), tools=[EchoTool()])

        result = runtime.run(Task("echo hello architecture"))

        self.assertFalse(result.succeeded)
        self.assertIn("Expected objective format", result.output)
        self.assertEqual([event.kind for event in result.events], ["planned"])

    def test_unknown_tool_returns_failure_event(self) -> None:
        runtime = Runtime(planner=PrefixPlanner(), tools=[EchoTool()])

        result = runtime.run(Task("missing: payload"))

        self.assertFalse(result.succeeded)
        self.assertEqual(result.output, "Tool not found: missing")
        self.assertEqual([event.kind for event in result.events], ["planned", "tool_missing"])

    def test_blank_task_is_rejected(self) -> None:
        runtime = Runtime(planner=PrefixPlanner(), tools=[EchoTool()])

        result = runtime.run(Task("  "))

        self.assertFalse(result.succeeded)
        self.assertEqual(result.output, "Task objective must not be blank.")
        self.assertEqual(result.events[0].kind, "task_invalid")


if __name__ == "__main__":
    unittest.main()
