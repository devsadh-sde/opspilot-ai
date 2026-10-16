
from pydantic import ValidationError

from app.schemas.customer_request import CustomerRequest


def main():
    # Test a valid customer request.
    valid_data = {
        "product_name": "Dell Latitude",
        "quantity": 20,
        "deadline": "2026-10-20",
        "budget": "15000.00",
    }

    request = CustomerRequest.model_validate(valid_data)

    print("Valid request:")
    print(request.model_dump_json(indent=2))

    # Test an invalid customer request.
    invalid_data = {
        "product_name": "Dell Latitude",
        "quantity": -5,
        "budget": "15000.00",
    }

    try:
        CustomerRequest.model_validate(invalid_data)
    except ValidationError as error:
        print("\nValidation error:")
        print(error.errors()[0]["msg"])


if __name__ == "__main__":
    main()
