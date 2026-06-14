from openviking_mini import EchoTool, PrefixPlanner, Runtime, Task


def main() -> None:
    runtime = Runtime(planner=PrefixPlanner(), tools=[EchoTool()])

    result = runtime.run(Task("echo: hello architecture"))

    print(result.output)
    print(",".join(event.kind for event in result.events))


if __name__ == "__main__":
    main()
