
from app.services.fulfillment_planner import create_fulfillment_plan


def main():
    # Test 1: Enough warehouse inventory
    plan = create_fulfillment_plan(product_id=1, quantity=15)

    assert plan["status"] == "feasible"
    assert plan["allocated_quantity"] == 15
    assert plan["unfulfilled_quantity"] == 0
    assert all(a["source"] == "warehouse" for a in plan["allocations"])

    print("Test 1 passed: Warehouse stock sufficient")

    # Test 2: Supplier needed
    plan = create_fulfillment_plan(product_id=1, quantity=25)

    assert plan["status"] == "feasible"
    assert plan["allocated_quantity"] == 25

    warehouse_qty = sum(
        a["quantity"] for a in plan["allocations"]
        if a["source"] == "warehouse"
    )
    supplier_qty = sum(
        a["quantity"] for a in plan["allocations"]
        if a["source"] == "supplier"
    )

    assert warehouse_qty == 20
    assert supplier_qty == 5

    print("Test 2 passed: Warehouse + supplier allocation")

    # Test 3: Insufficient total stock
    plan = create_fulfillment_plan(product_id=1, quantity=60)

    assert plan["status"] == "insufficient_stock"
    assert plan["allocated_quantity"] == 50
    assert plan["unfulfilled_quantity"] == 10

    print("Test 3 passed: Insufficient stock detected")
    print("\nAll fulfillment planner tests passed!")


if __name__ == "__main__":
    main()
