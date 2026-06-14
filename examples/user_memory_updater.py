from openviking_mini import InMemoryContextStore, SessionSummary, UserMemoryUpdater


def main() -> None:
    store = InMemoryContextStore()
    summary = SessionSummary(
        user_id="alice",
        objective="Answer architecture question",
        outcome="answered",
        user_feedback="Prefer concise answers.",
    )
    update = UserMemoryUpdater().apply(store, summary)

    if update is not None:
        print(update.uri)
        print(update.layers.abstract)


if __name__ == "__main__":
    main()
