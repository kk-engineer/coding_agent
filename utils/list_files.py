from pathlib import Path


def list_files(root="."):

    files = []

    for path in Path(root).rglob("*"):

        if path.is_file():
            files.append(str(path))

    return files