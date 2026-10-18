
from decimal import Decimal

from app.services.order_analysis_service import analyze_order
from app.services.policy_enforcement_service import evaluate_policies


def main():
    # Test 1: Within budget, sufficient stock
    analysis = analyze_order(
        product_id=1,
        quantity=10,
        budget=Decimal("20000")
    )

    result = evaluate_policies(analysis)

    assert result["human_approval_required"] is True
    assert result["customer_confirmation_required"] is False
    assert result["eligible_for_approval"] is True

    print("Test 1 passed: Eligible for human approval")

    # Test 2: Customer budget exceeded
    analysis = analyze_order(
        product_id=1,
        quantity=25,
        budget=Decimal("20000")
    )

    result = evaluate_policies(analysis)

    assert result["supplier_procurement_cost"] == "3100.00"
    assert result["customer_confirmation_required"] is True
    assert result["eligible_for_approval"] is False

    print("Test 2 passed: Customer confirmation required")

    # Test 3: Manager approval threshold exceeded
    analysis = analyze_order(
        product_id=1,
        quantity=40,
        budget=Decimal("100000")
    )

    result = evaluate_policies(analysis)

    assert result["supplier_procurement_cost"] == "12400.00"
    assert result["manager_approval_required"] is True
    assert result["human_approval_required"] is True

    print("Test 3 passed: Manager approval required")

    print("\nAll policy enforcement tests passed!")


if __name__ == "__main__":
    main()
