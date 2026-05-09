import sys

from command.cli import dispatch_command
from command.command_router import ParsedCommand, parse_command
from command.commands import Command
from command.handlers import handle_test
from utils.test_runner import run_tests


def test_test_command_runs_detected_test_command(monkeypatch):

    calls = {}

    def fake_detect_test_command():

        return "pytest"

    def fake_run_tests(command):

        calls["command"] = command

        return {
            "success": True,
            "stdout": "2 passed",
            "stderr": "",
            "returncode": 0
        }

    def fake_print_panel(content, title, border_style):

        calls["content"] = content
        calls["title"] = title
        calls["border_style"] = border_style

    monkeypatch.setattr(
        "command.handlers.detect_test_command",
        fake_detect_test_command
    )
    monkeypatch.setattr(
        "command.handlers.run_tests",
        fake_run_tests
    )
    monkeypatch.setattr(
        "command.handlers.print_markdown_panel",
        fake_print_panel
    )

    handle_test()

    assert calls["command"] == "pytest"
    assert calls["content"] == "2 passed"
    assert calls["title"] == "Test Results: pytest"
    assert calls["border_style"] == "green"


def test_dispatch_test_command_uses_test_handler(monkeypatch):

    calls = {"handled": False}

    def fake_handle_test():

        calls["handled"] = True

    monkeypatch.setattr(
        "command.cli.handle_test",
        fake_handle_test
    )

    should_exit = dispatch_command(
        ParsedCommand(command=Command.TEST)
    )

    assert should_exit is False
    assert calls["handled"] is True


def test_run_tests_reports_success_and_stdout():

    result = run_tests(
        f"{sys.executable} -c \"print('ok')\""
    )

    assert result["success"] is True
    assert result["returncode"] == 0
    assert result["stdout"].strip() == "ok"


def test_run_tests_reports_failure_and_stderr():

    result = run_tests(
        f"{sys.executable} -c \"import sys; sys.stderr.write('bad'); sys.exit(3)\""
    )

    assert result["success"] is False
    assert result["returncode"] == 3
    assert result["stderr"] == "bad"


def test_bang_alias_runs_local_command():

    parsed = parse_command("! echo hello")

    assert parsed.command == Command.RUN
    assert parsed.argument == "echo hello"


def test_freeform_explain_dispatches_without_edit(monkeypatch):

    calls = {
        "edit": 0,
        "explain": 0
    }

    def fake_handle_edit(argument):

        calls["edit"] += 1

    def fake_handle_explain(argument):

        calls["explain"] += 1
        calls["argument"] = argument

    monkeypatch.setattr(
        "command.cli.handle_edit",
        fake_handle_edit
    )
    monkeypatch.setattr(
        "command.cli.handle_explain",
        fake_handle_explain
    )

    parsed = parse_command("explain the code base")
    should_exit = dispatch_command(parsed)

    assert should_exit is False
    assert calls["edit"] == 0
    assert calls["explain"] == 1
    assert calls["argument"] == "."


def test_freeform_plan_dispatches_without_edit(monkeypatch):

    calls = {
        "edit": 0,
        "plan": 0
    }

    def fake_handle_edit(argument):

        calls["edit"] += 1

    def fake_handle_plan(argument):

        calls["plan"] += 1
        calls["argument"] = argument

    monkeypatch.setattr(
        "command.cli.handle_edit",
        fake_handle_edit
    )
    monkeypatch.setattr(
        "command.cli.handle_plan",
        fake_handle_plan
    )

    parsed = parse_command("plan how to add OAuth support")
    should_exit = dispatch_command(parsed)

    assert should_exit is False
    assert calls["edit"] == 0
    assert calls["plan"] == 1
    assert calls["argument"] == "plan how to add OAuth support"
