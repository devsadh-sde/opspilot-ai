
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discover available MCP tools.
            tools = await session.list_tools()

            print("\nAvailable MCP tools:")
            for tool in tools.tools:
                print(f"- {tool.name}")

            # Execute our inventory tool through MCP.
            result = await session.call_tool(
                "get_warehouse_inventory",
                arguments={"product_id": 1},
            )

            if result.isError:
                raise RuntimeError(
                    f"MCP tool returned an error: {result.content}"
                )

            print("\nInventory tool response:")
            for content in result.content:
                if content.type == "text":
                    print(content.text)


if __name__ == "__main__":
    asyncio.run(main())
