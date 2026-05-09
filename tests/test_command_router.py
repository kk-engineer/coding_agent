from command.command_router import parse_command
from command.commands import Command


def test_slash_opens_help():

    parsed = parse_command("/")

    assert parsed.command == Command.HELP
    assert parsed.error is None


def test_change_request_defaults_to_edit_instruction():

    parsed = parse_command("add token validation")

    assert parsed.command == Command.EDIT
    assert parsed.argument == "add token validation"
    assert parsed.freeform is True


def test_freeform_explain_codebase_is_read_only():

    parsed = parse_command("explain the code base")

    assert parsed.command == Command.EXPLAIN
    assert parsed.argument == "."
    assert parsed.freeform is True


def test_freeform_explain_file_targets_file():

    parsed = parse_command("explain file core/orchestrator.py")

    assert parsed.command == Command.EXPLAIN
    assert parsed.argument == "core/orchestrator.py"


def test_freeform_plan_is_read_only():

    parsed = parse_command("plan how to add OAuth support")

    assert parsed.command == Command.PLAN
    assert parsed.argument == "plan how to add OAuth support"
    assert parsed.freeform is True


def test_command_aliases_are_resolved():

    parsed = parse_command("/q")

    assert parsed.command == Command.EXIT


def test_test_alias_is_resolved():

    parsed = parse_command("/tests")

    assert parsed.command == Command.TEST


def test_missing_required_argument_returns_usage_error():

    parsed = parse_command("/plan")

    assert parsed.command == Command.PLAN
    assert parsed.error == "Usage: /plan <instruction>"
