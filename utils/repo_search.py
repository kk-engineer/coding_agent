import subprocess


def repo_search(query):

    result = subprocess.run(
        ["rg", "-n", query],
        capture_output=True,
        text=True
    )

    return result.stdout