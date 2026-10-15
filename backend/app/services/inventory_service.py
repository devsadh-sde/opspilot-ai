from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Inventory

def get_inventory(session: Session, product_id: int):
    statement = select(Inventory).where(
        Inventory.product_id == product_id
    )

    result = session.scalars(statement)

    return result.all()