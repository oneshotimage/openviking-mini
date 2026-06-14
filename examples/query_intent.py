from openviking_mini import KeywordIntentAnalyzer


def main() -> None:
    intent = KeywordIntentAnalyzer().analyze("Find the OpenViking context memory")
    print(intent.query)
    print(",".join(intent.terms))


if __name__ == "__main__":
    main()
