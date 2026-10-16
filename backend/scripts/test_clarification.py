
from app.schemas.customer_request import CustomerRequest
from app.services.clarification_service import (
    get_clarification_question,
)


def main():
    # Scenario 1: Product is missing.
    request1 = CustomerRequest(quantity=10)

    question1 = get_clarification_question(request1)
    print("Scenario 1:", question1)

    assert question1 == "Which product would you like to order?"

    # Scenario 2: Quantity is missing.
    request2 = CustomerRequest(
        product_name="Dell Latitude laptops"
    )

    question2 = get_clarification_question(request2)
    print("Scenario 2:", question2)

    assert question2 == (
        "How many units of Dell Latitude laptops would you like?"
    )

    # Scenario 3: All required information is available.
    request3 = CustomerRequest(
        product_name="Dell Latitude laptops",
        quantity=20,
    )

    question3 = get_clarification_question(request3)
    print("Scenario 3:", question3)

    assert question3 is None

    print("\nAll clarification tests passed!")


if __name__ == "__main__":
    main()
