from openviking_mini import ContextLayer, MemoryUpdate, SessionSummary, VikingURI


def main() -> None:
    summary = SessionSummary(user_id="alice", objective="answer question", outcome="answered")
    update = MemoryUpdate(
        uri=VikingURI.parse("viking://user/alice/memories/preferences/concise"),
        layers=ContextLayer(
            abstract="prefers concise answers",
            overview="Alice prefers concise answers.",
            details="Alice prefers concise answers when asking architecture questions.",
        ),
        reason="User feedback indicated a concise style preference.",
    )

    print(summary.user_id)
    print(update.uri)
    print(update.reason)


if __name__ == "__main__":
    main()
