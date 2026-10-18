
from app.services.policy_enforcement_service import evaluate_policies
from app.workflows.order_state import OrderState


def policy_enforcement_node(state: OrderState) -> dict:
    # Step 1: Read the completed order analysis.
    order_analysis = state["order_analysis"]

    # Step 2: Evaluate business rules.
    policy_evaluation = evaluate_policies(order_analysis)

    # Step 3: Determine the approval status.
    if not policy_evaluation["stock_sufficient"]:
        approval_status = "blocked_insufficient_stock"

    elif policy_evaluation["customer_confirmation_required"]:
        approval_status = "awaiting_customer_confirmation"

    elif policy_evaluation["manager_approval_required"]:
        approval_status = "awaiting_manager_approval"

    else:
        approval_status = "pending_human_approval"

    # Step 4: Return updates to LangGraph shared state.
    return {
        "policy_evaluation": policy_evaluation,
        "approval_status": approval_status
    }
