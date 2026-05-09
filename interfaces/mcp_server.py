from mcp.server.fastmcp import FastMCP

import config.agent_config
# MUST happen BEFORE other imports
config.agent_config.INTERFACE_MODE = "mcp"

from command.services import (
    get_diff,
    get_help,
    get_status,
    list_files_for_command,
    run_detected_tests,
    run_local_command,
    search_repository
)
from core.orchestrator import plan_changes, execute_changes
from core.chat import answer_chat
from core.explainer import explain_file
from utils.token_usage import get_token_usage, reset_token_usage

mcp = FastMCP("coding-agent")


def with_token_usage(result):

    if isinstance(result, dict):

        wrapped = dict(result)
        wrapped["token_usage"] = get_token_usage()
        return wrapped

    return {
        "result": result,
        "token_usage": get_token_usage()
    }


@mcp.tool()
def help():

    """
    Show available coding-agent commands.
    """

    reset_token_usage()
    return with_token_usage(get_help())


@mcp.tool()
async def chat(prompt: str):

    """
    Ask a read-only question without planning or editing.
    """

    reset_token_usage()
    result = await answer_chat(prompt)
    return with_token_usage(result)


@mcp.tool()
async def plan(prompt: str):

    """
    Create execution plan for repo changes.
    """

    reset_token_usage()
    result = await plan_changes(
        prompt,
        include_diffs=True
    )
    return with_token_usage(result)


@mcp.tool()
async def edit(prompt: str):

    """
    Modify repository files.
    """

    reset_token_usage()
    result = await execute_changes(prompt)
    return with_token_usage(result)


@mcp.tool()
def search(query: str):

    """
    Search repository code.
    """

    reset_token_usage()
    return with_token_usage(search_repository(query))


@mcp.tool()
def test(command: str | None = None):

    """
    Run tests.
    """

    reset_token_usage()
    return with_token_usage(run_detected_tests(command))


@mcp.tool()
def diff():

    """
    Show the current git diff.
    """

    reset_token_usage()
    return with_token_usage(get_diff())


@mcp.tool()
def files(path: str = "."):

    """
    List repository files under a path.
    """

    reset_token_usage()
    return with_token_usage(list_files_for_command(path))


@mcp.tool()
def pwd():

    """
    Show current workspace path.
    """

    reset_token_usage()
    return with_token_usage(get_status()["path"])


@mcp.tool()
def run(command: str):

    """
    Run a local command.
    """

    reset_token_usage()
    return with_token_usage(run_local_command(command))


@mcp.tool()
def status():

    """
    Show workspace, project, git, and test status.
    """

    reset_token_usage()
    return with_token_usage(get_status())


@mcp.tool()
def clear():

    """
    No-op for protocol clients; terminal clear is CLI-only.
    """

    reset_token_usage()
    return with_token_usage({
        "success": True,
        "message": "Clear is only meaningful in the interactive CLI."
    })

@mcp.tool()
async def explain(path: str):

    """
    Explain code in a file.
    """
    reset_token_usage()
    result = await explain_file(path)
    return with_token_usage(result)


def main():
    mcp.run()


if __name__ == "__main__":

    main()
