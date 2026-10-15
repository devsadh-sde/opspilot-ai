
from fastapi import APIRouter, HTTPException

from app.database.connection import SessionLocal
from app.services.supplier_service import get_supplier_offers


router = APIRouter()


@router.get("/suppliers/{product_id}")
def read_supplier_offers(product_id: int):
    with SessionLocal() as session:
        offers = get_supplier_offers(
            session=session,
            product_id=product_id
        )

        if not offers:
            raise HTTPException(
                status_code=404,
                detail="Supplier offers not found"
            )

        return {
            "product_id": product_id,
            "offers": [
                {
                    "supplier_id": offer.supplier_id,
                    "available_quantity": offer.available_quantity,
                    "unit_cost": str(offer.unit_cost),
                    "lead_time_days": offer.lead_time_days
                }
                for offer in offers
            ]
        }
