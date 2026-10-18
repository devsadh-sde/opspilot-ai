
from app.database.connection import SessionLocal
from app.services.product_service import find_product_by_name


def main():
    with SessionLocal() as session:

        # Test 1: Product exists
        product = find_product_by_name(session, "laptop")

        assert product is not None
        assert product.name == "High-End Laptop"

        print("Test 1 passed!")
        print(f"Found product: {product.name}")
        print(f"Product ID: {product.id}")

        # Test 2: Product does not exist
        missing_product = find_product_by_name(
            session, "Dell Latitude"
        )

        assert missing_product is None

        print("\nTest 2 passed!")
        print("Dell Latitude was not found in the database.")

    print("\nAll product lookup tests passed!")


if __name__ == "__main__":
    main()
