from utils.repo_search import (
    repo_search
)

from repo_utils.repo_scanner import (
    scan_repo
)


IGNORE_EXTENSIONS = {
    ".7z",
    ".avif",
    ".bmp",
    ".db",
    ".dll",
    ".dylib",
    ".eot",
    ".exe",
    ".gif",
    ".gz",
    ".ico",
    ".jar",
    ".jpeg",
    ".jpg",
    ".lockb",
    ".mp3",
    ".mp4",
    ".o",
    ".otf",
    ".pdf",
    ".png",
    ".pyc",
    ".rar",
    ".so",
    ".tar",
    ".wasm",
    ".webp",
    ".woff",
    ".woff2",
    ".zip",
}


GENERATED_FILE_NAMES = {
    "Cargo.lock",
    "Gemfile.lock",
    "composer.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "poetry.lock",
    "uv.lock",
    "yarn.lock",
}


GENERATED_PATH_PARTS = {
    ".next",
    ".nuxt",
    ".svelte-kit",
    "coverage",
    "dist",
    "generated",
    "node_modules",
    "public",
    "target",
}


GENERATED_SUFFIXES = (
    ".generated.css",
    ".generated.js",
    ".gen.go",
    ".min.css",
    ".min.js",
)


def is_generated_file(file_path: str):

    parts = set(file_path.split("/"))
    file_name = file_path.split("/")[-1]

    if file_name in GENERATED_FILE_NAMES:

        return True

    if parts & GENERATED_PATH_PARTS:

        return True

    return file_path.endswith(GENERATED_SUFFIXES)


def filter_code_files(files):

    """
    Keep only code/text files.
    """

    filtered = []

    for file in files:

        if is_generated_file(file):

            continue

        if any(
            file.endswith(ext)
            for ext in IGNORE_EXTENSIONS
        ):
            continue

        filtered.append(file)

    return filtered


def find_related_files(
    user_prompt
):

    """
    Repo-wide keyword search.

    Used for:
    - planning
    - execution
    - impact analysis
    """

    keywords = user_prompt.split()

    matches = []

    for keyword in keywords:

        result = repo_search(keyword)

        if result:

            for line in result.splitlines():

                try:

                    file_name = line.split(":")[0]

                    matches.append(file_name)

                except Exception:
                    pass

    matches = list(dict.fromkeys(matches))

    matches = filter_code_files(
        matches
    )

    return matches


def get_repository_files():

    """
    Return all repo files.
    """

    files = scan_repo()

    return filter_code_files(files)
