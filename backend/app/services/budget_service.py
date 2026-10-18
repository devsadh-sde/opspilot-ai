
from decimal import Decimal

from sqlalchemy.orm import Session

from app.database.models import Product
from app.services.pricing_service import validate_budget


def evaluate_order_budget(
    session: Session,
    product_id: int,
    quantity: int,
    budget: Decimal | None
) -> dict:

    if type(product_id) is not int or product_id <= 0:
        raise ValueError("Product ID must be positive")

    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Quantity must be positive")

    if budget is not None and budget < 0:
        raise ValueError("Budget cannot be negative")

    product = session.get(Product, product_id)

    if product is None:
        raise ValueError("Product not found")

    unit_price = Decimal(str(product.selling_price))
    total_price = unit_price * quantity

    within_budget = (
        validate_budget(total_price, budget)
        if budget is not None
        else None
    )

    return {
        "product_id": product_id,
        "quantity": quantity,
        "unit_price": str(unit_price),
        "total_price": str(total_price),
        "budget": str(budget) if budget is not None else None,
        "within_budget": within_budget
    }
