from pathlib import Path


def read_file(path):
    return Path(path).read_text()


def write_file(path, content):
    Path(path).write_text(content)