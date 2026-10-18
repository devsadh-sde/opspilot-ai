
from app.rag.policy_retriever import retrieve_policies
from app.workflows.order_state import OrderState


def policy_node(state: OrderState) -> dict:
    product_name = state.get("product_name")
    quantity = state.get("quantity")
    budget = state.get("budget")
    deadline = state.get("deadline")

    # Build a search query from customer requirements.
    query = (
        f"Order fulfillment policies for {quantity} "
        f"units of {product_name}. "
        f"Customer budget: {budget}. "
        f"Delivery deadline: {deadline}. "
        "Supplier procurement approval, warehouse "
        "fulfillment, pricing restrictions, and delivery."
    )

    # Retrieve relevant business policies.
    policies = retrieve_policies(
        query=query,
        top_k=5
    )

    return {
    "policies": policies
    }
