import unittest

from openviking_mini import ContextLayer, MemoryUpdate, MemoryUpdateError, SessionSummary, VikingURI


class MemoryContractTests(unittest.TestCase):
    def test_session_summary_requires_core_fields(self) -> None:
        summary = SessionSummary(user_id="alice", objective="answer question", outcome="answered")

        self.assertEqual(summary.user_id, "alice")
        self.assertEqual(summary.tool_notes, ())

    def test_session_summary_rejects_blank_core_fields(self) -> None:
        with self.assertRaisesRegex(MemoryUpdateError, "objective"):
            SessionSummary(user_id="alice", objective=" ", outcome="answered")

    def test_memory_update_requires_memory_uri(self) -> None:
        update = MemoryUpdate(
            uri=VikingURI.parse("viking://user/alice/memories/preferences/concise"),
            layers=ContextLayer(abstract="prefers concise answers", overview="prefers concise answers", details="prefers concise answers"),
            reason="User feedback said concise answers are preferred.",
        )

        self.assertEqual(update.uri.user_id, "alice")

    def test_memory_update_rejects_resource_uri(self) -> None:
        with self.assertRaisesRegex(MemoryUpdateError, "memory"):
            MemoryUpdate(
                uri=VikingURI.parse("viking://resources/openviking/docs/readme"),
                layers=ContextLayer(abstract="a", overview="b", details="c"),
                reason="not memory",
            )


if __name__ == "__main__":
    unittest.main()
