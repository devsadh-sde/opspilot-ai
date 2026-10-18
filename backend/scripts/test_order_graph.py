
from app.workflows.order_graph import order_graph


def main():
    # Test 1: Complete request with budget exceeded
    print("\n--- Test 1: Complete Order ---")

    result = order_graph.invoke({
        "customer_message": (
            "I need 25 High-End Laptop units "
            "with a budget of $20000."
        )
    })

    # Extract results from LangGraph shared state
    analysis = result["order_analysis"]
    fulfillment = analysis["fulfillment"]
    pricing = analysis["pricing"]
    print("\n--- DEBUG: LangGraph State ---")
    print("Available keys:", list(result.keys()))
    print("Final status:", result.get("status"))
    print("Question:", result.get("question"))
    print("Order analysis:", result.get("order_analysis"))
    policies = result["policies"]

    print("\n--- Order Analysis ---")
    print("Product ID:", result["product_id"])
    print("Requested quantity:", result["quantity"])
    print("Status:", result["status"])
    print("Allocations:", fulfillment["allocations"])
    print("Total price:", pricing["total_price"])
    print("Within budget:", pricing["within_budget"])

    # Validate product and overall status
    assert result["product_id"] == 1
    assert result["quantity"] == 25
    assert result["status"] == "over_budget"

    # Validate fulfillment allocation
    assert fulfillment["allocated_quantity"] == 25
    assert fulfillment["unfulfilled_quantity"] == 0

    warehouse_qty = sum(
        item["quantity"]
        for item in fulfillment["allocations"]
        if item["source"] == "warehouse"
    )

    supplier_qty = sum(
        item["quantity"]
        for item in fulfillment["allocations"]
        if item["source"] == "supplier"
    )

    assert warehouse_qty == 20
    assert supplier_qty == 5

    # Validate pricing and budget
    assert pricing["total_price"] == "37500.00"
    assert pricing["within_budget"] is False

    # Validate Policy RAG results
    print("\n--- Retrieved Business Policies ---")

    for policy in policies:
        print("Source:", policy["metadata"]["source"])
        print("Policy:", policy["document"])
        print("---")

    assert len(policies) > 0

    assert all(
        policy["document"].strip()
        for policy in policies
    )

    print("\nTest 1 passed!")

    # Test 2: Missing required information
    print("\n--- Test 2: Incomplete Request ---")

    result = order_graph.invoke({
        "customer_message": "I need laptops."
    })

    print("Status:", result["status"])
    print("Question:", result.get("question"))

    assert result["status"] == "needs_clarification"
    assert result["question"]
    assert result.get("order_analysis") is None
    assert result.get("policies") is None

    print("\nTest 2 passed!")

    print("\nAll LangGraph tests passed!")


if __name__ == "__main__":
    main()
