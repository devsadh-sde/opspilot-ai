
from decimal import Decimal

from app.services.order_analysis_service import analyze_order
from app.workflows.order_state import OrderState


def planning_node(state: OrderState) -> dict:
    # Step 1: Read extracted customer information.
    product_id = state["product_id"]
    quantity = state["quantity"]
    budget = state.get("budget")

    # Step 2: Convert budget to Decimal.
    budget_decimal = (
        Decimal(budget)
        if budget is not None
        else None
    )

    # Step 3: Calculate fulfillment and pricing.
    analysis = analyze_order(
        product_id=product_id,
        quantity=quantity,
        budget=budget_decimal
    )

    # Step 4: Update LangGraph shared state.
    return {
        "order_analysis": analysis,
        "status": analysis["status"]
    }
