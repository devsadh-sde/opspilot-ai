
from app.agents.inventory_agent import run_inventory_agent


def main():
    print("\n--- Testing Inventory Agent ---")

    result = run_inventory_agent(product_id=1)

    print("\n--- Agent Response ---")
    print(result)

    assert isinstance(result, str)
    assert result.strip()
    print("\nInventory Agent test passed!")


if __name__ == "__main__":
    main()
