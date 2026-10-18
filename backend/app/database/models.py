
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


# 1. Product
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    selling_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )


# 2. Warehouse
class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


# 3. Inventory
class Inventory(Base):
    __tablename__ = "inventory"

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "warehouse_id",
            name="uq_inventory_product_warehouse"
        ),
        CheckConstraint(
            "quantity >= 0",
            name="ck_inventory_quantity"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )


# 4. Supplier
class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )


# 5. Supplier Offer
class SupplierOffer(Base):
    __tablename__ = "supplier_offers"

    __table_args__ = (
        UniqueConstraint(
            "supplier_id",
            "product_id",
            name="uq_supplier_product_offer"
        ),
        CheckConstraint(
            "available_quantity >= 0",
            name="ck_supplier_available_quantity"
        ),
        CheckConstraint(
            "lead_time_days >= 0",
            name="ck_supplier_lead_time"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id"),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    available_quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    unit_cost: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    lead_time_days: Mapped[int] = mapped_column(
        nullable=False
    )


# 6. Order Proposal (NEW)
class OrderProposal(Base):
    __tablename__ = "order_proposals"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending_review",
        nullable=False
    )

    analysis_json: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
