import unittest

from openviking_mini import AccessScope, ContextLayer, ContextNode, InMemoryContextStore, RecursiveRetriever, RetrievalError, VikingURI


class AccessScopeTests(unittest.TestCase):
    def test_user_scope_allows_public_resources_and_own_user_context(self) -> None:
        scope = AccessScope(user_id="alice")

        self.assertTrue(scope.allows(VikingURI.parse("viking://resources/openviking/docs")))
        self.assertTrue(scope.allows(VikingURI.parse("viking://user/alice/resources/private/readme")))
        self.assertFalse(scope.allows(VikingURI.parse("viking://user/bob/resources/private/readme")))

    def test_retriever_rejects_denied_starting_path(self) -> None:
        store = InMemoryContextStore()
        store.add_node(_node("viking://user/bob/resources/private/readme"))

        with self.assertRaisesRegex(RetrievalError, "Access denied"):
            RecursiveRetriever(store, access_scope=AccessScope(user_id="alice")).retrieve(
                "private",
                VikingURI.parse("viking://user/bob/resources/private"),
            )

    def test_retriever_allows_own_user_resource_results(self) -> None:
        store = InMemoryContextStore()
        store.add_node(_node("viking://user/alice/resources/private/readme"))

        results = RecursiveRetriever(store, access_scope=AccessScope(user_id="alice")).retrieve(
            "private",
            VikingURI.parse("viking://user/alice/resources"),
        )

        self.assertEqual(tuple(str(result.uri) for result in results), ("viking://user/alice/resources/private/readme",))


def _node(raw_uri: str) -> ContextNode:
    return ContextNode(
        uri=VikingURI.parse(raw_uri),
        layers=ContextLayer(abstract="private", overview="private context", details="private details"),
    )


if __name__ == "__main__":
    unittest.main()
