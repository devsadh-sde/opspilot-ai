
from decimal import Decimal

from app.ai.request_extractor import extract_customer_request
from app.database.connection import SessionLocal
from app.services.clarification_service import get_clarification_question
from app.services.product_service import find_product_by_name
from app.services.order_analysis_service import analyze_order


def process_customer_request(customer_message: str) -> dict:

    # Step 1: Extract customer information using Claude.
    request = extract_customer_request(customer_message)

    # Step 2: Check whether clarification is needed.
    question = get_clarification_question(request)

    if question is not None:
        return {
            "status": "needs_clarification",
            "request": request.model_dump(mode="json"),
            "question": question
        }

    # Step 3: Find the requested product in SQLite.
    with SessionLocal() as session:
        product = find_product_by_name(
            session=session,
            product_name=request.product_name
        )

        if product is None:
            return {
                "status": "product_not_found",
                "request": request.model_dump(mode="json"),
                "question": (
                    f"We couldn't find '{request.product_name}' "
                    "in our catalog. Could you specify another product?"
                )
            }

        product_id = product.id

    # Step 4: Analyze inventory, suppliers, pricing, and budget.
    order_analysis = analyze_order(
        product_id=product_id,
        quantity=request.quantity,
        budget=(
            Decimal(str(request.budget))
            if request.budget is not None
            else None
        )
    )

    # Step 5: Return the complete structured analysis.
    return {
        "status": "analysis_complete",
        "request": request.model_dump(mode="json"),
        "product_id": product_id,
        "question": None,
        "order_analysis": order_analysis
    }
