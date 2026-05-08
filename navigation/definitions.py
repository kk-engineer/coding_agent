import jedi


def find_definition(
    source: str,
    path: str,
    line: int,
    column: int
):

    """
    Go-to-definition support.
    """

    script = jedi.Script(
        source,
        path=path
    )

    definitions = script.goto(
        line=line,
        column=column
    )

    results = []

    for d in definitions:

        results.append({
            "name": d.name,
            "module": d.module_name,
            "path": d.module_path,
            "line": d.line,
            "column": d.column,
            "type": d.type
        })

    return results