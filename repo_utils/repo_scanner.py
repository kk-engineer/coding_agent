from pathlib import Path

from config.agent_config import (
    WORKSPACE_ROOT
)

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


IGNORE_FILES = {
    ".DS_Store"
}


def should_ignore(path):

    """
    Ignore noisy/system directories.
    """

    if any(
        ignored in path.parts
        for ignored in IGNORE_DIRS
    ):

        return True

    if path.name in IGNORE_FILES:

        return True

    return False


def scan_repo(root=None):

    """
    Recursively scan repository files.
    """

    files = []

    scan_root = Path(root or WORKSPACE_ROOT)

    for path in scan_root.rglob("*"):

        if should_ignore(path):

            continue

        if path.is_file():

            files.append(
                str(path)
            )

    return files


def scan_python_files(root="."):

    """
    Scan only Python files.
    """

    files = []

    for path in Path(root).rglob("*.py"):

        if should_ignore(path):

            continue

        files.append(
            str(path)
        )

    return files


def scan_files_by_extensions(
    extensions: set[str],
    root="."
):

    """
    Scan files matching any extension.
    """

    files = []

    for path in Path(root).rglob("*"):

        if should_ignore(path):

            continue

        if path.is_file() and path.suffix in extensions:

            files.append(
                str(path)
            )

    return files


def build_repo_tree(root="."):

    """
    Build lightweight repo tree.
    """

    tree = {}

    for path in Path(root).rglob("*"):

        if should_ignore(path):

            continue

        parts = path.parts

        current = tree

        for part in parts:

            current = current.setdefault(
                part,
                {}
            )

    return tree
