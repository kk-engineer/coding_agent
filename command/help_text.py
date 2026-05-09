from command.commands import COMMAND_SPECS


def build_help_text() -> str:

    lines = [
        "Available Commands",
        "━━━━━━━━━━━━━━━━━━",
        "",
        "Tip: read-only questions stay read-only.",
        "Tip: change requests run as /edit.",
        "Tip: type / to show this menu.",
        "",
    ]

    for spec in COMMAND_SPECS.values():

        lines.append(spec.usage)
        lines.append(f"    {spec.description}")

        if spec.aliases:

            lines.append(
                f"    Aliases: {', '.join(spec.aliases)}"
            )

        if spec.example:

            lines.append(f"    Example: {spec.example}")

        lines.append("")

    return "\n".join(lines).rstrip()


HELP_TEXT = build_help_text()
