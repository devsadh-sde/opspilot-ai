
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _get_inventory_async(product_id: int) -> dict:
    """
    Connect to the OpsPilot MCP server and retrieve inventory.
    """

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "get_warehouse_inventory",
                arguments={"product_id": product_id},
            )

            if result.isError:
                raise RuntimeError(
                    f"MCP inventory lookup failed: {result.content}"
                )

            # Prefer structured MCP results when available.
            structured = getattr(result, "structuredContent", None)

            if isinstance(structured, dict):
                return structured

            # MCP SDK 1.x may return the dictionary as JSON text.
            import json

            for item in result.content:
                if item.type == "text":
                    return json.loads(item.text)

            raise RuntimeError(
                "MCP server returned no usable inventory data."
            )


def get_inventory_via_mcp(product_id: int) -> dict:
    """
    Synchronous wrapper for our current synchronous LangGraph node.
    """
    if product_id <= 0:
        raise ValueError("product_id must be positive")

    return asyncio.run(_get_inventory_async(product_id))
