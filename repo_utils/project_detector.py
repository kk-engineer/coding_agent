from pathlib import Path


PROJECT_MARKERS = (
    ("python", ("pyproject.toml", "setup.py", "requirements.txt", "Pipfile")),
    ("frontend/node", ("package.json", "pnpm-lock.yaml", "yarn.lock")),
    ("hugo", ("hugo.toml", "hugo.yaml", "hugo.json", "config.toml", "config.yaml")),
    ("docsy", ("themes/docsy", "assets/scss", "layouts/partials")),
    ("rust", ("Cargo.toml",)),
    ("go", ("go.mod",)),
    ("java", ("pom.xml", "build.gradle", "build.gradle.kts")),
    ("dotnet", ("*.csproj", "*.fsproj", "*.sln")),
    ("php", ("composer.json",)),
    ("ruby", ("Gemfile",)),
    ("elixir", ("mix.exs",)),
    ("swift", ("Package.swift",)),
    ("dart", ("pubspec.yaml",)),
)


def has_marker(
    root_path: Path,
    markers: tuple[str, ...]
):

    for marker in markers:

        if "*" in marker:

            if any(root_path.glob(marker)):

                return True

            continue

        if (root_path / marker).exists():

            return True

    return False


def detect_project_type(
    root="."
):

    """
    Detect repository language/framework.
    """

    root_path = Path(root)

    detected = [
        project_type
        for project_type, markers in PROJECT_MARKERS
        if has_marker(root_path, markers)
    ]

    if not detected:

        return "unknown"

    return ", ".join(detected)


def detect_test_command(
    root="."
):

    """
    Detect correct test runner.
    """

    root_path = Path(root)

    if (root_path / "pytest.ini").exists():

        return "pytest"

    if (root_path / "pyproject.toml").exists():

        return "pytest"

    if (root_path / "package.json").exists():

        return "npm test"

    if has_marker(
        root_path,
        ("hugo.toml", "hugo.yaml", "hugo.json", "config.toml", "config.yaml")
    ):

        return "hugo --gc --minify"

    if (root_path / "Cargo.toml").exists():

        return "cargo test"

    if (root_path / "go.mod").exists():

        return "go test ./..."

    if (root_path / "pom.xml").exists():

        return "mvn test"

    if (
        (root_path / "build.gradle").exists()
        or (root_path / "build.gradle.kts").exists()
    ):

        return "./gradlew test"

    if any(root_path.glob("*.csproj")) or any(root_path.glob("*.sln")):

        return "dotnet test"

    if (root_path / "composer.json").exists():

        return "composer test"

    if (root_path / "Gemfile").exists():

        return "bundle exec rake test"

    if (root_path / "mix.exs").exists():

        return "mix test"

    if (root_path / "Package.swift").exists():

        return "swift test"

    if (root_path / "pubspec.yaml").exists():

        return "dart test"

    return None


def detect_lint_command(root="."):

    """
    Detect lint command.
    """

    root_path = Path(root)

    if (root_path / "pyproject.toml").exists():

        return "ruff check ."

    if (root_path / "package.json").exists():

        return "npm run lint"

    if has_marker(
        root_path,
        ("hugo.toml", "hugo.yaml", "hugo.json", "config.toml", "config.yaml")
    ):

        return "hugo --gc --minify"

    if (root_path / "Cargo.toml").exists():

        return "cargo clippy"

    if (root_path / "go.mod").exists():

        return "go vet ./..."

    if any(root_path.glob("*.csproj")) or any(root_path.glob("*.sln")):

        return "dotnet format --verify-no-changes"

    return None
