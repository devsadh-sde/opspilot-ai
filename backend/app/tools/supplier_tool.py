
from app.database.connection import SessionLocal
from app.services.supplier_service import get_supplier_offers


def check_suppliers(product_id: int) -> dict:
    if type(product_id) is not int or product_id <= 0:
        raise ValueError("Product ID must be a positive integer")

    with SessionLocal() as session:
        offers = get_supplier_offers(
            session=session,
            product_id=product_id
        )

        suppliers = [
            {
                "supplier_id": offer.supplier_id,
                "available_quantity": offer.available_quantity,
                "unit_cost": str(offer.unit_cost),
                "lead_time_days": offer.lead_time_days
            }
            for offer in offers
        ]

        return {
            "product_id": product_id,
            "suppliers": suppliers
        }
