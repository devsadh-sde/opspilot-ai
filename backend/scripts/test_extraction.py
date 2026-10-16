from app.ai.request_extractor import extract_customer_request


def main():
    customer_message = (
    "I need Dell Latitude laptops for my office."
)

    request = extract_customer_request(customer_message)

    print("\n--- Extracted Customer Request ---")
    print(request.model_dump_json(indent=2))


if __name__ == "__main__":
    main()