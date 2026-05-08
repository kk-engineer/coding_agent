import jedi


def find_references(
    source: str,
    path: str,
    line: int,
    column: int
):

    """
    Find all references/usages
    of symbol.
    """

    script = jedi.Script(
        source,
        path=path
    )

    refs = script.get_references(
        line=line,
        column=column
    )

    results = []

    for r in refs:

        results.append({
            "name": r.name,
            "module": r.module_name,
            "path": r.module_path,
            "line": r.line,
            "column": r.column
        })

    return results