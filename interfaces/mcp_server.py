from mcp.server.fastmcp import FastMCP

import config.agent_config
# MUST happen BEFORE other imports
config.agent_config.INTERFACE_MODE = "mcp"

from core.orchestrator import plan_changes, execute_changes
from utils.search_code import search_code
from utils.test_runner import run_tests
from command.explainer import explain_file
from utils.logger import log

mcp = FastMCP("coding-agent")


@mcp.tool()
async def plan(prompt: str):

    """
    Create execution plan for repo changes.
    """

    return await plan_changes(prompt)


@mcp.tool()
async def edit(prompt: str):

    """
    Modify repository files.
    """

    return await execute_changes(prompt)


@mcp.tool()
def search(query: str):

    """
    Search repository code.
    """

    return search_code(query)


@mcp.tool()
def test(command: str):

    """
    Run tests.
    """

    return run_tests(command)

@mcp.tool()
async def explain(path: str):

    """
    Explain code in a file.
    """
    return explain_file(path)


def main():
    mcp.run()


if __name__ == "__main__":

    main()