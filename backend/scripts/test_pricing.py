
from decimal import Decimal

from app.services.pricing_service import (
    calculate_selling_price, 
    calculate_order_total,
    validate_budget,
    )


def main():
    unit_cost = Decimal("620.00")
    margin = Decimal("0.20")

    selling_price = calculate_selling_price(
        unit_cost=unit_cost,
        margin=margin
    )

    profit = selling_price - unit_cost

    print(f"Unit Cost: ${unit_cost}")
    print(f"Target Margin: {margin * 100}%")
    print(f"Selling Price: ${selling_price}")
    print(f"Gross Profit: ${profit}")


def test_order_total():
    quote = calculate_order_total(
        unit_cost=Decimal("620.00"),
        margin=Decimal("0.20"),
        quantity=20
    )

    print("\n--- Order Quote ---")
    print(f"Quantity: {quote['quantity']}")
    print(f"Unit Price: ${quote['unit_price']}")
    print(f"Total Cost: ${quote['total_cost']}")
    print(f"Total Price: ${quote['total_price']}")
    print(f"Gross Profit: ${quote['gross_profit']}")

    assert quote["total_price"] == Decimal("15500.00")
    assert quote["gross_profit"] == Decimal("3100.00")


def test_budget_validation():
    total_price = Decimal("15500.00")

    # Scenario 1: Customer has enough budget.
    assert validate_budget(
        total_price,
        Decimal("16000.00")
    ) is True

    # Scenario 2: Customer has insufficient budget.
    assert validate_budget(
        total_price,
        Decimal("15000.00")
    ) is False

    print("Both budget validation tests passed!")


if __name__ == "__main__":
    main()
    test_order_total()
    test_budget_validation()

