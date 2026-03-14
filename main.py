import shlex

from cli.commands import default_commands, handle_help, handle_quit


def main() -> None:
    commands = default_commands()

    print("Assistant Bot")
    print(handle_help(commands))

    while True:
        try:
            user_input = input(">>> ").strip()
        except EOFError, KeyboardInterrupt:
            print()
            print(handle_quit())
            break

        if not user_input:
            continue

        try:
            parts = shlex.split(user_input)
        except ValueError:
            print("Invalid input: unmatched quotes.")
            continue

        cmd_name = parts[0].lower()

        if cmd_name in ("quit", "exit", "close"):
            print(handle_quit())
            break

        if cmd_name == "help":
            print(handle_help(commands))
            continue

        handler = commands.get(cmd_name)
        if handler is None:
            print(f"Unknown command: {cmd_name}")
            continue

        print(handler(*parts[1:]))


if __name__ == "__main__":
    main()
