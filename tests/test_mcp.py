import asyncio

from mcp import ClientSession

from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters
)


async def main():

    server_params = StdioServerParameters(

        command="uv",

        args=[
            "run",
            "python",
            "-m",
            "interfaces.mcp_server"
        ]
    )

    async with stdio_client(
        server_params
    ) as streams:

        read, write = streams

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            print("\n=== TOOLS ===\n")

            tools = await session.list_tools()

            for tool in tools.tools:

                print(tool.name)

            print("\n=== SEARCH TEST ===\n")

            result = await session.call_tool(
                "search",
                {
                    "query": "jwt"
                }
            )

            print(result)

            print("\n=== PLAN TEST ===\n")

            result = await session.call_tool(
                "plan",
                {
                    "prompt": "add JWT validation"
                }
            )

            print(result)

            print("\n=== EXPLAIN TEST ===\n")

            result = await session.call_tool(
                "explain",
                {
                    "path": "test_repo/auth.py"
                }
            )

            print(result)


if __name__ == "__main__":

    asyncio.run(main())