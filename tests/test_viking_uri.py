import unittest

from openviking_mini import ContextType, VikingURI, VikingURIError


class VikingURITests(unittest.TestCase):
    def test_parses_resources_path(self) -> None:
        uri = VikingURI.parse("viking://resources/project/docs")

        self.assertEqual(uri.raw, "viking://resources/project/docs")
        self.assertEqual(uri.parts, ("resources", "project", "docs"))
        self.assertEqual(uri.context_type, ContextType.RESOURCES)
        self.assertEqual(str(uri), "viking://resources/project/docs")

    def test_parses_user_memory_path_with_user_boundary(self) -> None:
        uri = VikingURI.parse("viking://user/alice/memories/preferences")

        self.assertEqual(uri.parts, ("user", "alice", "memories", "preferences"))
        self.assertEqual(uri.context_type, ContextType.USER_MEMORIES)
        self.assertEqual(uri.user_id, "alice")

    def test_parses_user_skills_and_peers_as_distinct_context_types(self) -> None:
        skills = VikingURI.parse("viking://user/alice/skills/search_code")
        peer = VikingURI.parse("viking://user/alice/peers/web-visitor/resources")

        self.assertEqual(skills.context_type, ContextType.USER_SKILLS)
        self.assertEqual(peer.context_type, ContextType.USER_PEERS)

    def test_rejects_user_path_without_user_id(self) -> None:
        with self.assertRaisesRegex(VikingURIError, "user id"):
            VikingURI.parse("viking://user")

    def test_rejects_unknown_top_level_context(self) -> None:
        with self.assertRaisesRegex(VikingURIError, "Unknown context type"):
            VikingURI.parse("viking://documents/project")

    def test_rejects_parent_segments(self) -> None:
        with self.assertRaisesRegex(VikingURIError, "Path traversal"):
            VikingURI.parse("viking://resources/../secret")


if __name__ == "__main__":
    unittest.main()
