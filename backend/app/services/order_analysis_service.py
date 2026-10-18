
from decimal import Decimal

from app.database.connection import SessionLocal
from app.services.fulfillment_planner import create_fulfillment_plan
from app.services.budget_service import evaluate_order_budget


def analyze_order(
    product_id: int,
    quantity: int,
    budget: Decimal | None = None
) -> dict:

    # Step 1: Calculate warehouse and supplier allocations.
    fulfillment = create_fulfillment_plan(
        product_id=product_id,
        quantity=quantity
    )

    # Step 2: Calculate pricing and budget feasibility.
    with SessionLocal() as session:
        pricing = evaluate_order_budget(
            session=session,
            product_id=product_id,
            quantity=quantity,
            budget=budget
        )

    # Step 3: Determine the overall analysis status.
    if fulfillment["status"] != "feasible":
        status = "insufficient_stock"
    elif pricing["within_budget"] is False:
        status = "over_budget"
    else:
        status = "ready_for_review"

    return {
        "status": status,
        "fulfillment": fulfillment,
        "pricing": pricing
    }
