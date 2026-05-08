import difflib


def generate_diff(old, new, filename):

    diff = difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        fromfile=f"{filename}_old",
        tofile=f"{filename}_new",
        lineterm=""
    )

    return "\n".join(diff)