
from app.tools.supplier_tool import check_suppliers
from app.workflows.order_state import OrderState


def supplier_node(state: OrderState) -> dict:
    # Step 1: Retrieve product ID from shared state.
    product_id = state["product_id"]

    # Step 2: Get actual supplier offers from SQLite.
    suppliers = check_suppliers(product_id=product_id)

    # Step 3: Update the LangGraph shared state.
    return {
        "suppliers": suppliers,
        "status": "suppliers_checked"
    }
