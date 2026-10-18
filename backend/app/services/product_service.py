
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Product


def find_product_by_name(
    session: Session,
    product_name: str
) -> Product | None:

    if not product_name.strip():
        raise ValueError("Product name cannot be empty")

    statement = select(Product).where(
        Product.name.ilike(f"%{product_name.strip()}%")
    )

    return session.scalar(statement)
