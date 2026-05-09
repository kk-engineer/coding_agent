from dataclasses import dataclass

from command.commands import (
    Command,
    get_command_spec,
    resolve_command
)


EXPLAIN_INTENTS = (
    "explain",
    "describe",
    "summarize",
    "walk me through",
    "what is",
    "what does",
    "how does",
    "show me how",
    "understand",
    "review the codebase",
    "review the code base",
)

PLAN_INTENTS = (
    "plan",
    "design",
    "approach",
    "strategy",
    "how should",
    "what would it take",
)

EDIT_INTENTS = (
    "add",
    "change",
    "create",
    "delete",
    "edit",
    "fix",
    "implement",
    "modify",
    "move",
    "refactor",
    "remove",
    "rename",
    "replace",
    "update",
    "write",
)


@dataclass(frozen=True)
class ParsedCommand:

    command: Command
    argument: str = ""
    raw_input: str = ""
    error: str | None = None
    freeform: bool = False


def parse_command(user_input: str) -> ParsedCommand:

    """
    Parse CLI commands.

    Slash-prefixed input is treated as a command. Plain text is treated as an
    edit instruction, mirroring common coding-agent CLIs.
    """

    raw_input = user_input
    user_input = user_input.strip()

    if not user_input:

        return ParsedCommand(
            command=Command.NOOP,
            raw_input=raw_input
        )

    if not user_input.startswith("/") and not user_input.startswith("!"):

        command, argument = infer_freeform_command(user_input)

        return ParsedCommand(
            command=command,
            argument=argument,
            raw_input=raw_input,
            freeform=True
        )

    parts = user_input.split(
        " ",
        1
    )

    command = parts[0]

    argument = ""

    if len(parts) > 1:

        argument = parts[1]

    resolved = resolve_command(command)

    if resolved == Command.UNKNOWN:

        return ParsedCommand(
            command=Command.UNKNOWN,
            argument=argument,
            raw_input=raw_input,
            error=f"Unknown command: {command}"
        )

    spec = get_command_spec(resolved)

    if spec and spec.requires_argument and not argument:

        return ParsedCommand(
            command=resolved,
            argument=argument,
            raw_input=raw_input,
            error=f"Usage: {spec.usage}"
        )

    return ParsedCommand(
        command=resolved,
        argument=argument,
        raw_input=raw_input
    )


def infer_freeform_command(user_input: str) -> tuple[Command, str]:

    """
    Infer intent for natural-language CLI input.

    Read-only requests must stay read-only. Editing is only the default when the
    prompt looks like a change request or the intent is otherwise ambiguous.
    """

    lowered = user_input.lower().strip()

    if _starts_with_intent(lowered, EXPLAIN_INTENTS):

        return Command.EXPLAIN, extract_explain_target(user_input)

    if _starts_with_intent(lowered, PLAN_INTENTS):

        return Command.PLAN, user_input

    if _starts_with_intent(lowered, EDIT_INTENTS):

        return Command.EDIT, user_input

    return Command.EDIT, user_input


def extract_explain_target(user_input: str) -> str:

    lowered = user_input.lower().strip()

    broad_targets = (
        "codebase",
        "code base",
        "repo",
        "repository",
        "project",
        "app",
        "application",
    )

    if any(target in lowered for target in broad_targets):

        return "."

    for marker in (" file ", " module ", " directory ", " folder "):

        if marker in lowered:

            _, target = user_input.split(
                marker.strip(),
                1
            )

            cleaned = target.strip()

            if cleaned:

                return cleaned

    return "."


def _starts_with_intent(
    value: str,
    intents: tuple[str, ...]
) -> bool:

    return any(
        value == intent
        or value.startswith(f"{intent} ")
        for intent in intents
    )
