
from decimal import Decimal, ROUND_HALF_UP


def calculate_selling_price(
    unit_cost: Decimal,
    margin: Decimal
) -> Decimal:

    if unit_cost < 0:
        raise ValueError("Unit cost cannot be negative")

    if not Decimal("0") <= margin < Decimal("1"):
        raise ValueError("Margin must be between 0 and 1 (exclusive)")

    selling_price = unit_cost / (Decimal("1") - margin)

    return selling_price.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

def calculate_order_total(
    unit_cost: Decimal,
    margin: Decimal,
    quantity: int
) -> dict:

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    selling_price = calculate_selling_price(
        unit_cost=unit_cost,
        margin=margin
    )

    total_cost = unit_cost * quantity
    total_price = selling_price * quantity
    gross_profit = total_price - total_cost

    return {
        "quantity": quantity,
        "unit_price": selling_price,
        "total_cost": total_cost,
        "total_price": total_price,
        "gross_profit": gross_profit
    }


def validate_budget(
    total_price: Decimal,
    budget: Decimal
) -> bool:

    if budget < 0:
        raise ValueError("Budget cannot be negative")

    if total_price < 0:
        raise ValueError("Total price cannot be negative")

    return total_price <= budget
