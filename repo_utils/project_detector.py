from pathlib import Path


def detect_project_type(
    root="."
):

    """
    Detect repository language/framework.
    """

    if Path("pyproject.toml").exists():

        return "python"

    if Path("package.json").exists():

        return "node"

    if Path("Cargo.toml").exists():

        return "rust"

    if Path("pom.xml").exists():

        return "java"

    return "unknown"


def detect_test_command(
    root="."
):

    """
    Detect correct test runner.
    """

    if Path("pytest.ini").exists():

        return "pytest"

    if Path("pyproject.toml").exists():

        return "pytest"

    if Path("package.json").exists():

        return "npm test"

    if Path("Cargo.toml").exists():

        return "cargo test"

    if Path("pom.xml").exists():

        return "mvn test"

    return "pytest"


def detect_lint_command():

    """
    Detect lint command.
    """

    if Path("pyproject.toml").exists():

        return "ruff check ."

    if Path("package.json").exists():

        return "npm run lint"

    return None