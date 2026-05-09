from command.services import (
    get_status,
    list_files_for_command,
    run_detected_tests,
    run_local_command,
    search_repository
)


def test_run_local_command_returns_structured_result():

    result = run_local_command("echo hello")

    assert result["success"] is True
    assert result["stdout"].strip() == "hello"
    assert result["returncode"] == 0


def test_run_detected_tests_accepts_missing_command():

    result = run_detected_tests(command=None)

    assert "success" in result
    assert "command" in result


def test_list_files_for_command(tmp_path):

    file_path = tmp_path / "index.html"
    file_path.write_text("<h1>Hello</h1>")

    assert list_files_for_command(str(tmp_path)) == [str(file_path)]


def test_search_repository_returns_list():

    assert isinstance(search_repository("def"), list)


def test_get_status_returns_protocol_shape():

    status = get_status()

    assert {"path", "project", "test_command", "branch", "git"} <= set(status)
