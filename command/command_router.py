from command.commands import Command


def parse_command(user_input: str):

    """
    Parse CLI commands.
    """

    user_input = user_input.strip()

    if not user_input:

        return None, None

    parts = user_input.split(
        " ",
        1
    )

    command = parts[0]

    argument = ""

    if len(parts) > 1:

        argument = parts[1]

    try:

        return Command(command), argument

    except Exception:

        return None, user_input