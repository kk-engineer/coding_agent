from command.command_router import ParsedCommand, parse_command
from command.commands import Command
from command.handlers import (
    handle_clear,
    handle_diff,
    handle_edit,
    handle_explain,
    handle_files,
    handle_help,
    handle_plan,
    handle_pwd,
    handle_run,
    handle_search,
    handle_status,
    handle_test
)
from command.help_text import HELP_TEXT
from utils.console import console
from utils.token_usage import get_token_usage, reset_token_usage


PROMPT = "[bold cyan]agent[/bold cyan]> "


def run_cli():

    console.print(
        "[bold green]Coding Agent Ready[/bold green]"
    )

    console.print(
        (
            "Type [bold]/[/bold] for commands, ask read-only questions, "
            "or describe a change.\n"
        )
    )

    while True:

        try:

            user_input = console.input(PROMPT)

        except (EOFError, KeyboardInterrupt):

            console.print("\n[green]Goodbye[/green]")
            break

        parsed = parse_command(user_input)

        if parsed.command == Command.NOOP:

            continue

        if parsed.error:

            console.print(f"[red]{parsed.error}[/red]")
            continue

        try:

            reset_token_usage()

            should_exit = dispatch_command(parsed)

        except KeyboardInterrupt:

            console.print("\n[green]Goodbye[/green]")
            break

        print_token_usage()

        if should_exit:

            break


def print_token_usage():

    usage = get_token_usage()

    console.print(
        "[dim]Tokens: "
        f"prompt={usage['prompt_tokens']}, "
        f"completion={usage['completion_tokens']}, "
        f"total={usage['total_tokens']}[/dim]"
    )


def dispatch_command(parsed: ParsedCommand) -> bool:

    if parsed.command == Command.HELP:

        handle_help(HELP_TEXT)

    elif parsed.command == Command.PLAN:

        handle_plan(parsed.argument)

    elif parsed.command == Command.EDIT:

        handle_edit(parsed.argument)

    elif parsed.command == Command.EXPLAIN:

        handle_explain(parsed.argument)

    elif parsed.command == Command.SEARCH:

        handle_search(parsed.argument)

    elif parsed.command == Command.TEST:

        handle_test()

    elif parsed.command == Command.DIFF:

        handle_diff()

    elif parsed.command == Command.FILES:

        handle_files(parsed.argument)

    elif parsed.command == Command.PWD:

        handle_pwd()

    elif parsed.command == Command.RUN:

        handle_run(parsed.argument)

    elif parsed.command == Command.STATUS:

        handle_status()

    elif parsed.command == Command.CLEAR:

        handle_clear()

    elif parsed.command == Command.EXIT:

        console.print(
            "[green]Goodbye[/green]"
        )

        return True

    elif parsed.command == Command.UNKNOWN:

        console.print(
            "[red]Unknown command[/red]"
        )

    return False
