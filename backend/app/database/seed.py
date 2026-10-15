from decimal import Decimal

from sqlalchemy import select

from app.database.connection import (
    Base,
    SessionLocal,
    engine,
)

from app.database.models import (
    Inventory,
    Product,
    Supplier,
    SupplierOffer,
    Warehouse,
)

def seed_database():
    #create tables if they do not exist.
    Base.metadata.create_all(bind=engine)

    #Start a database session.
    with SessionLocal.begin() as session:

        #Avoid inserting duplicate demo data.
        existing = session.scalar(
            select(Product.id).limit(1)
        )

        if existing is not None:
            print("Database already has products.")
            return

        #Create one product.
        laptop = Product(
            sku="LAPTOP-001",
            name="High-End Laptop",
            category="Electronics",
            selling_price=Decimal("1500.00"),
        )

        #Create two warehouses.
        houston = Warehouse(
            name="Houston Warehouse",
            city="Houston",
        )

        dallas = Warehouse(
            name = "Dallas Warehouse",
            city="Dallas",
        )

        #Create a supplier.
        supplier = Supplier(
            name = "TechSource Distribution"
        )

        session.add_all([
            laptop,
            houston,
            dallas,
            supplier,
        ])

        #Assign database IDs before referencing them
        session.flush()

        #Add warehouse inventory.
        session.add_all([
            Inventory(
                product_id=laptop.id,
                warehouse_id=houston.id,
                quantity = 12,
            ),
            Inventory(
                product_id=laptop.id,
                warehouse_id=dallas.id,
                quantity=8,
            ),
        ])

        #Add a supplier offer
        session.add(
            SupplierOffer(
                product_id=laptop.id,
                supplier_id=supplier.id,
                available_quantity=30,
                unit_cost = Decimal("620.00"),
                lead_time_days=3,
            )
        )

        print("Northstar Electronics database seeded!")

if __name__ == "__main__":
    seed_database()

