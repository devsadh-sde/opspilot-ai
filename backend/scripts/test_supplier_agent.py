
from app.agents.supplier_agent import run_supplier_agent


def main():
    print("\n--- Testing Supplier Agent ---")

    result = run_supplier_agent(product_id=1)

    print("\n--- Supplier Agent Response ---")
    print(result)

    assert isinstance(result, str)
    assert result.strip()

    print("\nSupplier Agent test passed!")


if __name__ == "__main__":
    main()
