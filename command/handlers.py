import asyncio
import shlex
import subprocess
from pathlib import Path

from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from command.commands import COMMAND_SPECS
from core.approval import is_approved
from core.explainer import explain_path
from config.agent_config import MAX_PLAN_DIFF_FILES
from core.orchestrator import (
    execute_changes,
    generate_suggested_diffs,
    plan_changes
)
from repo_utils.project_detector import detect_project_type, detect_test_command
from utils.console import console
from utils.file_ops import list_directory
from utils.panel import print_markdown_panel
from utils.search_code import search_code
from utils.test_runner import run_tests


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
        limit=MAX_PLAN_DIFF_FILES
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

    if len(results) > 20:

        console.print(
            f"[dim]Showing 20 of {len(results)} matches.[/dim]"
        )


def handle_test():

    test_command = detect_test_command()
    result = run_tests(test_command)
    output = result["stdout"] or result["stderr"] or "No test output."
    style = "green" if result["success"] else "red"

    print_markdown_panel(
        output,
        title=f"Test Results: {test_command}",
        border_style=style
    )


def handle_diff():

    diff = _git_output(["git", "diff"])

    if not diff:

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


def handle_files(argument: str = "."):

    root = argument or "."

    try:

        files = list_directory(root)

    except Exception as e:

        console.print(f"[red]{e}[/red]")
        return

    visible_files = [
        file_path
        for file_path in files
        if Path(file_path).is_file()
    ]

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

        command = shlex.split(argument)

    except ValueError as e:

        console.print(f"[red]Invalid command: {e}[/red]")
        return

    if not command:

        console.print("[red]Usage: /run <command>[/red]")
        return

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False
    )

    output = result.stdout or result.stderr or "No output."
    style = "green" if result.returncode == 0 else "red"

    print_markdown_panel(
        output,
        title=f"Command exited {result.returncode}",
        border_style=style
    )


def handle_status():

    cwd = Path.cwd()
    project_type = detect_project_type()
    test_command = detect_test_command()
    branch = _git_output(["git", "branch", "--show-current"]) or "unknown"
    status = _git_output(["git", "status", "--short"])
    status_text = status if status else "clean"

    console.print("[bold]Workspace[/bold]")
    console.print(f"  Path: {cwd}")
    console.print(f"  Project: {project_type}")
    console.print(f"  Test command: {test_command}")
    console.print(f"  Branch: {branch}")
    console.print(f"  Git: {status_text}")


def handle_clear():

    console.clear()


def _git_output(command: list[str]) -> str:

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

    except OSError:

        return ""

    if result.returncode != 0:

        return ""

    return result.stdout.strip()
