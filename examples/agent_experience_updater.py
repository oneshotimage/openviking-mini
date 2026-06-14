from openviking_mini import AgentExperienceUpdater, InMemoryContextStore, SessionSummary


def main() -> None:
    store = InMemoryContextStore()
    summary = SessionSummary(
        user_id="alice",
        objective="Answer architecture question",
        outcome="answered",
        tool_notes=("Use grep before find.", "Keep retrieval scoped."),
    )
    update = AgentExperienceUpdater().apply(store, summary)

    if update is not None:
        print(update.uri)
        print(update.layers.details)


if __name__ == "__main__":
    main()
