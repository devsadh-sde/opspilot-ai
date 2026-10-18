
from decimal import Decimal

from app.database.connection import SessionLocal
from app.services.budget_service import evaluate_order_budget


def main():
    with SessionLocal() as session:

        # Test 1: Budget is sufficient
        result = evaluate_order_budget(
            session=session,
            product_id=1,
            quantity=10,
            budget=Decimal("20000")
        )

        assert result["total_price"] == "15000.00"
        assert result["within_budget"] is True

        print("Test 1 passed: Within budget")

        # Test 2: Budget is exceeded
        result = evaluate_order_budget(
            session=session,
            product_id=1,
            quantity=25,
            budget=Decimal("20000")
        )

        assert result["total_price"] == "37500.00"
        assert result["within_budget"] is False

        print("Test 2 passed: Budget exceeded")

        # Test 3: No budget provided
        result = evaluate_order_budget(
            session=session,
            product_id=1,
            quantity=5,
            budget=None
        )

        assert result["total_price"] == "7500.00"
        assert result["within_budget"] is None

        print("Test 3 passed: No budget provided")

    print("\nAll budget service tests passed!")


if __name__ == "__main__":
    main()
