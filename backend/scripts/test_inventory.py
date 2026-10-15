from app.database.connection import SessionLocal
from app.services.inventory_service import get_inventory

def main():
    with SessionLocal() as session:
        inventory_records = get_inventory(
            session = session,
            product_id = 1
        )

        total_quantity = 0

        for record in inventory_records:
            print(
                f"Warehouse ID: {record.warehouse_id}, "
                f"Quantity: {record.quantity}"
            )

            total_quantity += record.quantity

        print(f"Total Quantity: {total_quantity}")

if __name__ == "__main__":
    main()