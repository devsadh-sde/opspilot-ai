
from app.schemas.customer_request import CustomerRequest


def get_clarification_question(
    request: CustomerRequest
) -> str | None:

    if request.product_name is None:
        return "Which product would you like to order?"

    if request.quantity is None:
        return (
            "How many units of "
            f"{request.product_name} would you like?"
        )

    return None
