
from app.database.connection import SessionLocal
from app.services.product_service import find_product_by_name
from app.workflows.order_state import OrderState


def product_lookup_node(state: OrderState) -> dict:
    # Step 1: Read product name from shared state.
    product_name = state.get("product_name")

    if not product_name:
        return {
            "status": "needs_clarification",
            "question": "Which product would you like to order?"
        }

    # Step 2: Search the product catalog.
    with SessionLocal() as session:
        product = find_product_by_name(
            session=session,
            product_name=product_name
        )

        if product is None:
            return {
                "status": "product_not_found",
                "question": (
                    f"We couldn't find '{product_name}' "
                    "in our catalog. Could you specify another product?"
                )
            }

        product_id = product.id

    # Step 3: Update shared state.
    return {
        "product_id": product_id,
        "status": "product_found",
        "question": None
    }
