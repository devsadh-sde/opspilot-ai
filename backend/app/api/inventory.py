
from fastapi import APIRouter, HTTPException

from app.database.connection import SessionLocal
from app.services.inventory_service import get_inventory


router = APIRouter()


@router.get("/inventory/{product_id}")
def read_inventory(product_id: int):
    with SessionLocal() as session:
        records = get_inventory(
            session=session,
            product_id=product_id
        )

        if not records:
            raise HTTPException(
                status_code=404,
                detail="Inventory not found"
            )

        return {
            "product_id": product_id,
            "total_quantity": sum(
                record.quantity for record in records
            ),
            "warehouses": [
                {
                    "warehouse_id": record.warehouse_id,
                    "quantity": record.quantity
                }
                for record in records
            ]
        }
