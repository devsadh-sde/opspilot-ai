
from app.workflows.fulfillment_workflow import analyze_fulfillment


def main():
    print("\n--- Testing Fulfillment Workflow ---")

    result = analyze_fulfillment(product_id=1)

    print("\n--- Inventory Analysis ---")
    print(result["inventory_analysis"])

    print("\n--- Supplier Analysis ---")
    print(result["supplier_analysis"])

    assert result["product_id"] == 1
    assert result["inventory_analysis"].strip()
    assert result["supplier_analysis"].strip()

    print("\nFulfillment workflow test passed!")


if __name__ == "__main__":
    main()
