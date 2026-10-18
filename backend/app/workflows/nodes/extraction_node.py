
from app.ai.request_extractor import extract_customer_request
from app.services.clarification_service import get_clarification_question
from app.workflows.order_state import OrderState


def extraction_node(state: OrderState) -> dict:
    # Step 1: Read the customer message from shared state.
    customer_message = state["customer_message"]

    # Step 2: Extract structured information using Claude.
    request = extract_customer_request(customer_message)

    # Step 3: Check for missing required information.
    question = get_clarification_question(request)

    # Step 4: Return updates to LangGraph shared state.
    return {
        "product_name": request.product_name,
        "quantity": request.quantity,
        "budget": (
            str(request.budget)
            if request.budget is not None
            else None
        ),
        "deadline": (
            request.deadline.isoformat()
            if request.deadline is not None
            else None
        ),
        "status": (
            "needs_clarification"
            if question is not None
            else "extracted"
        ),
        "question": question
    }
