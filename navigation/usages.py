from navigation.references import (
    find_references
)


def find_usages(
    source: str,
    path: str,
    line: int,
    column: int
):

    """
    Alias for references.

    Used for:
    - find usages
    - impact analysis
    - refactoring
    """

    return find_references(
        source,
        path,
        line,
        column
    )