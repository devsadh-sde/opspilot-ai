
from app.tools.supplier_tool import check_suppliers


def main():
    result = check_suppliers(product_id=1)

    print("\n--- Supplier Tool Result ---")
    print(result)

    assert result["product_id"] == 1
    assert len(result["suppliers"]) == 1

    supplier = result["suppliers"][0]

    assert supplier["available_quantity"] == 30
    assert float(supplier["unit_cost"]) == 620.0
    assert supplier["lead_time_days"] == 3

    print("\nAll supplier tool tests passed!")


if __name__ == "__main__":
    main()
