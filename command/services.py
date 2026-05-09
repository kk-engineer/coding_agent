import shlex
import subprocess
from pathlib import Path

from command.help_text import HELP_TEXT
from repo_utils.project_detector import detect_project_type, detect_test_command
from utils.file_ops import list_directory
from utils.search_code import search_code
from utils.test_runner import run_tests


def get_help():

    return HELP_TEXT


def get_status():

    branch = run_git_command(["git", "branch", "--show-current"]) or "unknown"
    status = run_git_command(["git", "status", "--short"])

    return {
        "path": str(Path.cwd()),
        "project": detect_project_type(),
        "test_command": detect_test_command(),
        "branch": branch,
        "git": status if status else "clean"
    }


def get_diff():

    return run_git_command(["git", "diff"]) or "No unstaged changes."


def list_files_for_command(path: str = "."):

    root = path or "."
    files = list_directory(root)

    return [
        file_path
        for file_path in files
        if Path(file_path).is_file()
    ]


def search_repository(query: str):

    return search_code(query)


def run_detected_tests(command: str | None = None):

    return run_tests(
        command or detect_test_command()
    )


def run_local_command(command_text: str):

    try:

        command = shlex.split(command_text)

    except ValueError as e:

        return {
            "success": False,
            "stdout": "",
            "stderr": f"Invalid command: {e}",
            "returncode": 1
        }

    if not command:

        return {
            "success": False,
            "stdout": "",
            "stderr": "No command provided.",
            "returncode": 1
        }

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False
    )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }


def run_git_command(command: list[str]) -> str:

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
