from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key= True
    )

    sku: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(150), nullable= False
    )

    category: Mapped[str] = mapped_column(
        String(50), nullable= False
    )

    selling_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "selling_price >= 0",
            name = "ck_product_price"
        ),
    )

class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100), unique= True, nullable= False
    )

    city: Mapped[str] = mapped_column(
        String(100), nullable= False
    )

class Inventory(Base):
    __tablename__ = "inventory"

    id:Mapped[int] = mapped_column(
        primary_key = True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False
    )

    warehouse_id: Mapped[str] = mapped_column(
        ForeignKey("warehouses.id"), nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id", 
            "warehouse_id",
            name="uq_product_warehouse"
            ),
        CheckConstraint(
            "quantity >= 0",
            name="ck_inventory_quantity"
        ),
    )

class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(
        primary_key= True
    )

    name: Mapped[str] = mapped_column(
        String(100), unique= True, nullable= False
    )

class SupplierOffer(Base):
    __tablename__ = "supplier_offers"

    id: Mapped[int] = mapped_column(
        primary_key = True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False
    )   

    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id"), nullable=False
    )

    available_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    unit_cost: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )   

    lead_time_days: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "supplier_id",
            name="uq_product_supplier"
        ),
        CheckConstraint(
            "available_quantity >= 0",
            name="ck_supplier_offer_quantity"
        ),
        CheckConstraint(
            "unit_cost >= 0",
            name="ck_supplier_offer_unit_cost"
        ),
        CheckConstraint(
            "lead_time_days >= 0",
            name="ck_supplier_offer_lead_time"
        ),
    )
