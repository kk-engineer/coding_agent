from pathlib import Path


def read_file(path):

    path_obj = Path(path)

    if not path_obj.exists():

        raise FileNotFoundError(
            f"Path does not exist: {path}"
        )

    if path_obj.is_dir():

        raise IsADirectoryError(
            f"Expected file but got directory: {path}"
        )

    return path_obj.read_text()


def write_file(path, content):

    Path(path).write_text(content)


def list_directory(path):

    path_obj = Path(path)

    if not path_obj.exists():

        raise FileNotFoundError(
            f"Directory does not exist: {path}"
        )

    if not path_obj.is_dir():

        raise NotADirectoryError(
            f"Expected directory but got file: {path}"
        )

    files = []

    for item in path_obj.rglob("*"):

        # Ignore noisy dirs
        if any(
            ignored in item.parts
            for ignored in [
                ".git",
                "__pycache__",
                ".venv",
                "node_modules"
            ]
        ):
            continue

        files.append(str(item))

    return files