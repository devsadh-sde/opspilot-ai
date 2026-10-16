
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class CustomerRequest(BaseModel):
    product_name: str | None = Field(
        default=None,
        min_length=1
    )

    quantity: int | None = Field(
        default=None,
        gt=0,
        strict=True
)

    deadline: date | None = None

    budget: Decimal | None = Field(
        default=None,
        ge=0
    )
