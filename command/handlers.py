import asyncio
from pathlib import Path

from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from command.commands import COMMAND_SPECS
from command.services import (
    get_diff,
    get_status,
    list_files_for_command,
    run_detected_tests,
    run_local_command,
    search_repository
)
from core.approval import is_approved
from core.chat import answer_chat
from core.explainer import explain_path
from config.agent_config import MAX_PLAN_DIFF_FILES
from core.orchestrator import (
    execute_changes,
    generate_suggested_diffs,
    plan_changes
)
from utils.console import console
from utils.panel import print_markdown_panel


def handle_help(help_text: str):

    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=None,
        expand=True
    )
    table.add_column("Command", style="bold green", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Aliases", style="yellow")
    table.add_column("Example", style="dim")

    for spec in COMMAND_SPECS.values():

        table.add_row(
            Text(spec.usage),
            spec.description,
            Text(", ".join(spec.aliases)) if spec.aliases else "",
            spec.example or ""
        )

    help_tip = Text()
    help_tip.append("Tips: ", style="bold")
    help_tip.append("read-only questions stay read-only; ", style="cyan")
    help_tip.append("change requests run as /edit; ", style="green")
    help_tip.append("type / to reopen this menu.", style="yellow")

    content = Table.grid(
        expand=True
    )
    content.add_row(help_tip)
    content.add_row(table)

    console.print(
        Panel(
            content,
            title="[bold]Coding Agent Commands[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )
    )


def handle_plan(argument: str):

    result = asyncio.run(
        plan_changes(argument)
    )

    print_markdown_panel(
        result["plan"],
        title="Execution Plan",
        border_style="yellow"
    )

    related_files = result.get("related_files", [])

    if not related_files:

        return

    console.print(
        "[bold cyan][planning][/bold cyan] "
        "Generating suggested diffs without modifying files..."
    )

    suggested_diffs = generate_suggested_diffs(
        user_prompt=argument,
        files=related_files,
        limit=MAX_PLAN_DIFF_FILES,
        progress_callback=print_diff_progress
    )

    if not suggested_diffs:

        console.print(
            "[dim]No suggested diffs generated.[/dim]"
        )

        return

    for diff_entry in suggested_diffs:

        print_diff_panel(
            diff_entry["diff"],
            title=f"Suggested Diff: {diff_entry['file']}",
            border_style="magenta"
        )


def handle_chat(argument: str):

    response = asyncio.run(
        answer_chat(argument)
    )

    print_markdown_panel(
        response,
        title="Read-only Answer",
        border_style="blue"
    )


def handle_edit(argument: str):

    planning_result = asyncio.run(
        plan_changes(argument)
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

        print_diff_panel(
            diff_entry["diff"],
            title=diff_entry["file"],
            border_style="red"
        )

    tests = result.get("tests")

    if tests:

        style = "green" if tests["success"] else "red"
        output = tests["stdout"] or tests["stderr"] or "No test output."

        print_markdown_panel(
            output,
            title="Test Results",
            border_style=style
        )


def handle_explain(argument: str):

    explanation = asyncio.run(
        explain_path(argument)
    )

    print_markdown_panel(
        explanation,
        title=f"Explanation: {argument}",
        border_style="blue"
    )


def handle_search(argument: str):

    results = search_repository(argument)

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

    if len(results) > 20:

        console.print(
            f"[dim]Showing 20 of {len(results)} matches.[/dim]"
        )


def handle_test():

    result = run_detected_tests()
    test_command = result.get("command")
    output = result["stdout"] or result["stderr"] or "No test output."
    style = "green" if result["success"] else "red"

    print_markdown_panel(
        output,
        title=f"Test Results: {test_command}",
        border_style=style
    )


def handle_diff():

    diff = get_diff()

    if diff == "No unstaged changes.":

        console.print(
            Panel(
                "No unstaged changes.",
                title="[bold]Git Diff[/bold]",
                border_style="magenta"
            )
        )

        return

    console.print(
        Panel(
            Syntax(
                diff,
                "diff",
                word_wrap=True
            ),
            title="[bold]Git Diff[/bold]",
            border_style="magenta"
        )
    )


def print_diff_panel(
    diff: str,
    title: str,
    border_style: str
):

    console.print(
        Panel(
            Syntax(
                diff,
                "diff",
                word_wrap=True
            ),
            title=f"[bold]{title}[/bold]",
            border_style=border_style,
            padding=(1, 2)
        )
    )


def print_diff_progress(
    event: str,
    file_path: str,
    index: int,
    total: int
):

    if event == "start":

        console.print(
            f"[dim]({index}/{total}) Preparing suggested diff for "
            f"{file_path}...[/dim]"
        )

    elif event == "end":

        console.print(
            f"[dim]({index}/{total}) Finished {file_path}[/dim]"
        )


def handle_files(argument: str = "."):

    root = argument or "."

    try:

        visible_files = list_files_for_command(root)

    except Exception as e:

        console.print(f"[red]{e}[/red]")
        return

    for file_path in visible_files[:80]:

        console.print(file_path)

    if len(visible_files) > 80:

        console.print(
            f"[dim]Showing 80 of {len(visible_files)} files.[/dim]"
        )


def handle_pwd():

    console.print(str(Path.cwd()))


def handle_run(argument: str):

    try:

        result = run_local_command(argument)

    except Exception as e:

        console.print(f"[red]{e}[/red]")
        return

    output = result["stdout"] or result["stderr"] or "No output."
    style = "green" if result["success"] else "red"

    print_markdown_panel(
        output,
        title=f"Command exited {result['returncode']}",
        border_style=style
    )


def handle_status():

    status = get_status()

    console.print("[bold]Workspace[/bold]")
    console.print(f"  Path: {status['path']}")
    console.print(f"  Project: {status['project']}")
    console.print(f"  Test command: {status['test_command']}")
    console.print(f"  Branch: {status['branch']}")
    console.print(f"  Git: {status['git']}")


def handle_clear():

    console.clear()
