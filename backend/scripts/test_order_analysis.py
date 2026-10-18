
from decimal import Decimal

from app.services.order_analysis_service import analyze_order


def main():
    # Test 1: Enough inventory and sufficient budget
    result = analyze_order(
        product_id=1,
        quantity=10,
        budget=Decimal("20000")
    )

    assert result["status"] == "ready_for_review"
    assert result["fulfillment"]["allocated_quantity"] == 10
    assert result["pricing"]["within_budget"] is True

    print("Test 1 passed: Order ready for review")

    # Test 2: Enough inventory but insufficient budget
    result = analyze_order(
        product_id=1,
        quantity=25,
        budget=Decimal("20000")
    )

    assert result["status"] == "over_budget"
    assert result["fulfillment"]["allocated_quantity"] == 25
    assert result["pricing"]["within_budget"] is False

    print("Test 2 passed: Order exceeds budget")

    # Test 3: Insufficient total inventory
    result = analyze_order(
        product_id=1,
        quantity=60,
        budget=Decimal("100000")
    )

    assert result["status"] == "insufficient_stock"
    assert result["fulfillment"]["unfulfilled_quantity"] == 10

    print("Test 3 passed: Insufficient stock")

    print("\nAll order analysis tests passed!")


if __name__ == "__main__":
    main()
