import unittest

from openviking_mini import KeywordIntentAnalyzer, RetrievalError


class IntentAnalyzerTests(unittest.TestCase):
    def test_extracts_normalized_unique_terms(self) -> None:
        intent = KeywordIntentAnalyzer().analyze("What is OpenViking context context?")

        self.assertEqual(intent.query, "What is OpenViking context context?")
        self.assertEqual(intent.terms, ("openviking", "context"))

    def test_filters_small_stop_word_set(self) -> None:
        intent = KeywordIntentAnalyzer().analyze("find the memory for the user")

        self.assertEqual(intent.terms, ("memory", "user"))

    def test_rejects_blank_query(self) -> None:
        with self.assertRaisesRegex(RetrievalError, "query"):
            KeywordIntentAnalyzer().analyze(" ")

    def test_rejects_query_without_useful_terms(self) -> None:
        with self.assertRaisesRegex(RetrievalError, "terms"):
            KeywordIntentAnalyzer().analyze("the and for")


if __name__ == "__main__":
    unittest.main()
