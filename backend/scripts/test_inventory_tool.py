
from app.tools.inventory_tool import check_inventory


def main():
    # Scenario 1: Product with inventory
    result = check_inventory(product_id=1)

    print("\n--- Inventory Tool Result ---")
    print(result)

    assert result["product_id"] == 1
    assert result["total_quantity"] == 20
    assert len(result["warehouses"]) == 2

    print("\nAll inventory tool tests passed!")


if __name__ == "__main__":
    main()
