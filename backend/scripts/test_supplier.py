
from app.database.connection import SessionLocal
from app.services.supplier_service import get_supplier_offers


def main():
    with SessionLocal() as session:
        offers = get_supplier_offers(
            session=session,
            product_id=1
        )

        for offer in offers:
            print(f"Supplier ID: {offer.supplier_id}")
            print(f"Available: {offer.available_quantity}")
            print(f"Unit Cost: ${offer.unit_cost}")
            print(f"Lead Time: {offer.lead_time_days} days")


if __name__ == "__main__":
    main()
