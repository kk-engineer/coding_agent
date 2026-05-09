from dataclasses import dataclass
from enum import Enum


class Command(str, Enum):

    NOOP = "noop"

    UNKNOWN = "unknown"

    HELP = "/help"

    EDIT = "/edit"

    PLAN = "/plan"

    EXPLAIN = "/explain"

    SEARCH = "/search"

    TEST = "/test"

    DIFF = "/diff"

    FILES = "/files"

    PWD = "/pwd"

    RUN = "/run"

    STATUS = "/status"

    CLEAR = "/clear"

    EXIT = "/exit"


@dataclass(frozen=True)
class CommandSpec:

    command: Command
    usage: str
    description: str
    aliases: tuple[str, ...] = ()
    example: str | None = None
    requires_argument: bool = False


COMMAND_SPECS = {
    Command.HELP: CommandSpec(
        command=Command.HELP,
        usage="/help",
        description="Show commands and examples.",
        aliases=("/", "/?"),
    ),
    Command.EDIT: CommandSpec(
        command=Command.EDIT,
        usage="/edit <instruction>",
        description="Plan, confirm, and apply code changes.",
        aliases=("/do",),
        example="/edit add JWT validation",
        requires_argument=True,
    ),
    Command.PLAN: CommandSpec(
        command=Command.PLAN,
        usage="/plan <instruction>",
        description="Generate an execution plan without changing files.",
        example="/plan add OAuth support",
        requires_argument=True,
    ),
    Command.EXPLAIN: CommandSpec(
        command=Command.EXPLAIN,
        usage="/explain <path>",
        description="Explain a file or directory.",
        aliases=("/why",),
        example="/explain core/orchestrator.py",
        requires_argument=True,
    ),
    Command.SEARCH: CommandSpec(
        command=Command.SEARCH,
        usage="/search <query>",
        description="Search the repository.",
        aliases=("/find",),
        example="/search validate_token",
        requires_argument=True,
    ),
    Command.TEST: CommandSpec(
        command=Command.TEST,
        usage="/test",
        description="Run the detected test suite.",
        aliases=("/tests",),
    ),
    Command.DIFF: CommandSpec(
        command=Command.DIFF,
        usage="/diff",
        description="Show the current git diff.",
    ),
    Command.FILES: CommandSpec(
        command=Command.FILES,
        usage="/files [path]",
        description="List files under a path.",
        example="/files core",
    ),
    Command.PWD: CommandSpec(
        command=Command.PWD,
        usage="/pwd",
        description="Show the current workspace path.",
    ),
    Command.RUN: CommandSpec(
        command=Command.RUN,
        usage="/run <command>",
        description="Run a local command and show its output.",
        aliases=("!",),
        example="/run pytest",
        requires_argument=True,
    ),
    Command.STATUS: CommandSpec(
        command=Command.STATUS,
        usage="/status",
        description="Show workspace, git, and test-runner status.",
        aliases=("/st",),
    ),
    Command.CLEAR: CommandSpec(
        command=Command.CLEAR,
        usage="/clear",
        description="Clear the terminal.",
        aliases=("/cls",),
    ),
    Command.EXIT: CommandSpec(
        command=Command.EXIT,
        usage="/exit",
        description="Exit the coding agent.",
        aliases=("/quit", "/q"),
    ),
}


ALIASES = {
    alias: spec.command
    for spec in COMMAND_SPECS.values()
    for alias in spec.aliases
}


def resolve_command(token: str) -> Command:

    if token in ALIASES:

        return ALIASES[token]

    try:

        return Command(token)

    except ValueError:

        return Command.UNKNOWN


def get_command_spec(command: Command) -> CommandSpec | None:

    return COMMAND_SPECS.get(command)
