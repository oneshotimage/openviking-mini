import unittest

from openviking_mini import AgentExperienceUpdater, ContextLayer, InMemoryContextStore, MemoryUpdate, MemoryUpdateError, SessionSummary, UserMemoryUpdater, VikingURI


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

    def test_user_memory_updater_builds_update_from_feedback(self) -> None:
        summary = SessionSummary(
            user_id="alice",
            objective="Answer architecture question",
            outcome="answered",
            user_feedback="Prefer concise answers.",
        )

        update = UserMemoryUpdater().build_update(summary)

        self.assertIsNotNone(update)
        assert update is not None
        self.assertEqual(str(update.uri), "viking://user/alice/memories/session/answer-architecture-question")
        self.assertEqual(update.layers.abstract, "Prefer concise answers.")

    def test_user_memory_updater_skips_blank_feedback(self) -> None:
        summary = SessionSummary(user_id="alice", objective="Answer", outcome="answered")

        self.assertIsNone(UserMemoryUpdater().build_update(summary))

    def test_user_memory_updater_can_apply_to_store(self) -> None:
        store = InMemoryContextStore()
        summary = SessionSummary(
            user_id="alice",
            objective="Answer architecture question",
            outcome="answered",
            user_feedback="Prefer concise answers.",
        )

        update = UserMemoryUpdater().apply(store, summary)

        self.assertIsNotNone(update)
        self.assertEqual(store.read(VikingURI.parse("viking://user/alice/memories/session/answer-architecture-question"), layer="abstract"), "Prefer concise answers.")

    def test_agent_experience_updater_builds_update_from_tool_notes(self) -> None:
        summary = SessionSummary(
            user_id="alice",
            objective="Answer architecture question",
            outcome="answered",
            tool_notes=("Use grep before find.", "Keep retrieval scoped."),
        )

        update = AgentExperienceUpdater().build_update(summary)

        self.assertIsNotNone(update)
        assert update is not None
        self.assertEqual(str(update.uri), "viking://agent/memories/session/answer-architecture-question")
        self.assertEqual(update.layers.abstract, "Use grep before find.")
        self.assertIn("Keep retrieval scoped.", update.layers.details)

    def test_agent_experience_updater_skips_empty_tool_notes(self) -> None:
        summary = SessionSummary(user_id="alice", objective="Answer", outcome="answered")

        self.assertIsNone(AgentExperienceUpdater().build_update(summary))

    def test_agent_experience_updater_can_apply_to_store(self) -> None:
        store = InMemoryContextStore()
        summary = SessionSummary(
            user_id="alice",
            objective="Answer architecture question",
            outcome="answered",
            tool_notes=("Use grep before find.",),
        )

        update = AgentExperienceUpdater().apply(store, summary)

        self.assertIsNotNone(update)
        self.assertEqual(store.read(VikingURI.parse("viking://agent/memories/session/answer-architecture-question"), layer="abstract"), "Use grep before find.")


if __name__ == "__main__":
    unittest.main()
