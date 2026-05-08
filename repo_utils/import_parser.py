import re


IMPORT_RE = r"^\\s*import\\s+(.+)"

FROM_RE = r"^\\s*from\\s+(.+)\\s+import"


def parse_imports(content):

    """
    Extract imports from source file.

    Supports:
        import x
        from x import y
    """

    imports = []

    for line in content.splitlines():

        line = line.strip()

        m1 = re.match(
            IMPORT_RE,
            line
        )

        if m1:

            imports.append(
                m1.group(1)
            )

        m2 = re.match(
            FROM_RE,
            line
        )

        if m2:

            imports.append(
                m2.group(1)
            )

    return imports


def normalize_imports(
    imports
):

    """
    Normalize imports.

    Example:
        package.module
        -> package
    """

    normalized = []

    for imp in imports:

        normalized.append(
            imp.split(".")[0]
        )

    return normalized