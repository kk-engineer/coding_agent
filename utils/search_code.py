import subprocess
from pathlib import Path

from config.agent_config import (
    WORKSPACE_ROOT
)

root=WORKSPACE_ROOT


IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".pytest_cache",
    "dist",
    "build"
}


def build_rg_command(
    query: str,
    root: str = ".",
    file_pattern: str | None = None
):

    """
    Build ripgrep command safely.
    """

    command = [
        "rg",
        "-n",                   # show line numbers
        "--hidden",             # include hidden files
        "--glob", "!*.pyc"
    ]

    for ignored in IGNORE_DIRS:

        command.extend([
            "--glob",
            f"!{ignored}/**"
        ])

    if file_pattern:

        command.extend([
            "--glob",
            file_pattern
        ])

    command.append(query)

    command.append(root)

    return command


def search_code(
    query: str,
    root: str = ".",
    file_pattern: str | None = None
):

    """
    Repo-wide code search using ripgrep.

    Example:
        search_code(
            query=\"validate_token\"
        )

    Returns:
        [
            {
                \"file\": \"auth.py\",
                \"line\": 12,
                \"content\": \"def validate_token(...)\"
            }
        ]
    """

    command = build_rg_command(
        query=query,
        root=root,
        file_pattern=file_pattern
    )

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    matches = []

    for line in result.stdout.splitlines():

        try:

            parts = line.split(":", 2)

            if len(parts) < 3:
                continue

            file_path = parts[0]

            line_number = int(parts[1])

            content = parts[2]

            matches.append({
                "file": file_path,
                "line": line_number,
                "content": content.strip()
            })

        except Exception:
            pass

    return matches


def search_python_code(
    query: str,
    root: str = "."
):

    """
    Search only Python files.
    """

    return search_code(
        query=query,
        root=root,
        file_pattern="*.py"
    )


def search_symbol(
    symbol_name: str,
    root: str = "."
):

    """
    Search symbol definitions/usages.

    Useful for:
    - find usages
    - impact analysis
    - refactors
    """

    return search_python_code(
        query=symbol_name,
        root=root
    )