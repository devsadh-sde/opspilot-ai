
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import SupplierOffer


def get_supplier_offers(
    session: Session,
    product_id: int
):
    statement = select(SupplierOffer).where(
        SupplierOffer.product_id == product_id
    )

    result = session.scalars(statement)

    return result.all()
