
from app.database.connection import SessionLocal
from app.services.inventory_service import get_inventory


def check_inventory(product_id: int) -> dict:
    if product_id <= 0:
        raise ValueError("Product ID must be positive")

    with SessionLocal() as session:
        records = get_inventory(
            session=session,
            product_id=product_id
        )

        warehouses = [
            {
                "warehouse_id": record.warehouse_id,
                "quantity": record.quantity,
            }
            for record in records
        ]

        return {
            "product_id": product_id,
            "total_quantity": sum(
                record["quantity"] for record in warehouses
            ),
            "warehouses": warehouses,
        }
