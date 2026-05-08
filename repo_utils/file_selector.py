from utils.repo_search import (
    repo_search
)

from repo_utils.repo_scanner import (
    scan_repo
)


IGNORE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".pdf",
    ".zip",
    ".db"
}


def filter_code_files(files):

    """
    Keep only code/text files.
    """

    filtered = []

    for file in files:

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

    matches = list(set(matches))

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