
from mcp.server.fastmcp import FastMCP

from app.tools.inventory_tool import check_inventory


# Create the MCP server
mcp = FastMCP("OpsPilot AI")


@mcp.tool()
def get_warehouse_inventory(product_id: int) -> dict:
    """
    Retrieve current warehouse inventory for a product.

    Args:
        product_id: Database ID of the product.

    Returns:
        Warehouse stock quantities and total available units.
    """
    if product_id <= 0:
        raise ValueError("product_id must be positive")

    return check_inventory(product_id)


if __name__ == "__main__":
    mcp.run()
