
from app.workflows.request_workflow import (
    process_customer_request,
)


def main():
    # Scenario 1: Missing quantity.
    message1 = "I need Dell Latitude laptops."

    result1 = process_customer_request(message1)

    print("\n--- Scenario 1: Incomplete Request ---")
    print(result1)

    assert result1["status"] == "needs_clarification"
    assert result1["request"]["quantity"] is None
    assert result1["question"] is not None

    # Scenario 2: Complete essential information.
    message2 = "I need 20 Dell Latitude laptops."

    result2 = process_customer_request(message2)

    print("\n--- Scenario 2: Complete Request ---")
    print(result2)

    assert result2["status"] == "ready_for_analysis"
    assert result2["request"]["quantity"] == 20
    assert result2["question"] is None

    print("\nAll workflow tests passed!")


if __name__ == "__main__":
    main()
