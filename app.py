from rich.console import Console
from rich.panel import Panel

from utils.panel import (
    print_markdown_panel
)

from command.command_router import (
    parse_command
)

from command.commands import (
    Command
)

from command.help_text import (
    HELP_TEXT
)

from core.orchestrator import (
    plan_changes,
    execute_changes
)

from core.approval import (
    is_approved
)

from command.explainer import (
    explain_file
)

from utils.search_code import (
    search_code
)

from utils.test_runner import run_tests

import asyncio

console = Console()


def handle_plan(argument):
    result = asyncio.run(
        plan_changes(argument)
    )

    print_markdown_panel(
        result["plan"],
        title="Execution Plan",
        border_style="yellow"
    )


def handle_edit(argument):

    planning_result = plan_changes(
        argument
    )

    print_markdown_panel(
        planning_result["plan"],
        title="Execution Plan",
        border_style="cyan"
    )

    approval = input(
        "\nProceed with changes? [yes/no]: "
    )

    if not is_approved(approval):

        console.print(
            "[red]Changes cancelled.[/red]"
        )

        return

    result = asyncio.run(
        execute_changes(argument)
    )

    for step in result["steps"]:

        console.print(
            f"[yellow][{step['type']}][/yellow] "
            f"{step['content']}"
        )


    for diff_entry in result["diffs"]:

        print_markdown_panel(
            diff_entry["diff"],
            title=diff_entry["file"],
            border_style="red"
        )

def handle_explain(argument):


    explanation = explain_file(argument)

    print_markdown_panel(
        explanation,
        title=f"Explanation: {argument}",
        border_style="blue"
    )


def handle_search(argument):

    results = search_code(argument)

    if not results:

        console.print(
            "[red]No matches found[/red]"
        )

        return

    for result in results[:20]:

        console.print(
            f"[cyan]{result['file']}[/cyan]"
            f":{result['line']} "
            f"{result['content']}"
        )


def handle_test():

    result = run_tests()

    print_markdown_panel(
        result["stdout"],
        title=f"Test Results",
        border_style="green"
    )


def main():

    console.print(
        "[bold green]"
        "Coding Agent Ready"
        "[/bold green]"
    )

    console.print(
        "Type /help for commands\n"
    )

    while True:

        user_input = input("> ")

        command, argument = parse_command(
            user_input
        )

        if command == Command.HELP:

            console.print(HELP_TEXT)

        elif command == Command.PLAN:

            handle_plan(argument)

        elif command == Command.EDIT:

            handle_edit(argument)

        elif command == Command.EXPLAIN:

            handle_explain(argument)

        elif command == Command.SEARCH:

            handle_search(argument)

        elif command == Command.TEST:

            handle_test()

        elif command == Command.EXIT:

            console.print(
                "[green]Goodbye[/green]"
            )

            break

        else:

            console.print(
                "[red]Unknown command[/red]"
            )


if __name__ == "__main__":

    main()