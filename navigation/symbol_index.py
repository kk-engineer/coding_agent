from pathlib import Path
import jedi


IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules"
}


def build_symbol_index(
    root="."
):

    """
    Build repository-wide symbol index.
    """

    index = {}

    for path in Path(root).rglob("*.py"):

        if any(
            ignored in path.parts
            for ignored in IGNORE_DIRS
        ):
            continue

        try:

            source = path.read_text()

            script = jedi.Script(
                source,
                path=str(path)
            )

            names = script.get_names(
                all_scopes=True,
                definitions=True,
                references=False
            )

            index[str(path)] = [

                {
                    "name": n.name,
                    "type": n.type,
                    "line": n.line,
                    "column": n.column
                }

                for n in names
            ]

        except Exception:
            pass

    return index


def search_symbol(
    symbol_index,
    symbol_name
):

    """
    Search symbol in repository.
    """

    matches = []

    for file_path, symbols in symbol_index.items():

        for symbol in symbols:

            if symbol["name"] == symbol_name:

                matches.append({
                    "file": file_path,
                    **symbol
                })

    return matches