
from app.ai.request_extractor import extract_customer_request
from app.services.clarification_service import (
    get_clarification_question,
)


def process_customer_request(customer_message: str) -> dict:

    # Step 1: Extract information using Claude.
    request = extract_customer_request(customer_message)

    # Step 2: Check whether clarification is needed.
    question = get_clarification_question(request)

    # Step 3: Return a structured workflow result.
    if question is not None:
        return {
            "status": "needs_clarification",
            "request": request.model_dump(mode="json"),
            "question": question,
        }

    return {
        "status": "ready_for_analysis",
        "request": request.model_dump(mode="json"),
        "question": None,
    }
