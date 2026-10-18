
from app.mcp.client import get_inventory_via_mcp
from app.workflows.order_state import OrderState


def inventory_node(state: OrderState) -> dict:
    # Step 1: Get the product ID from LangGraph state.
    product_id = state["product_id"]

    # Step 2: Retrieve inventory through the MCP server.
    inventory = get_inventory_via_mcp(product_id=product_id)

    # Step 3: Update LangGraph state.
    return {
        "inventory": inventory,
        "status": "inventory_checked",
    }
