import subprocess


def run_tests(command=None):

    if not command:

        return {
            "success": False,
            "stdout": "",
            "stderr": "No test command detected for this project.",
            "returncode": 1,
            "command": command
        }

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
        "command": command
    }
