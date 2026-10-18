
from decimal import Decimal


def evaluate_policies(order_analysis: dict) -> dict:
    fulfillment = order_analysis["fulfillment"]
    pricing = order_analysis["pricing"]

    # Calculate supplier procurement cost.
    supplier_cost = Decimal("0")

    for allocation in fulfillment["allocations"]:
        if allocation["source"] == "supplier":
            supplier_cost += (
                Decimal(allocation["unit_cost"])
                * allocation["quantity"]
            )

    # Evaluate approval requirements.
    manager_approval_required = supplier_cost > Decimal("10000")

    customer_confirmation_required = (
        pricing["within_budget"] is False
    )

    stock_sufficient = (
        fulfillment["status"] == "feasible"
    )

    return {
        "supplier_procurement_cost": str(supplier_cost),
        "manager_approval_required": manager_approval_required,
        "customer_confirmation_required": customer_confirmation_required,
        "human_approval_required": True,
        "stock_sufficient": stock_sufficient,
        "eligible_for_approval": (
            stock_sufficient
            and not customer_confirmation_required
        )
    }
