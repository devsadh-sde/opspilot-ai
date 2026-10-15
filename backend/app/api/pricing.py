
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.pricing_service import calculate_order_total


router = APIRouter()


class PricingRequest(BaseModel):
    unit_cost: Annotated[Decimal, Field(ge=0)]
    margin: Annotated[Decimal, Field(ge=0, lt=1)]
    quantity: Annotated[int, Field(gt=0, strict=True)]


@router.post("/pricing/quote")
def create_quote(request: PricingRequest):
    quote = calculate_order_total(
        unit_cost=request.unit_cost,
        margin=request.margin,
        quantity=request.quantity
    )

    return {
        "quantity": quote["quantity"],
        "unit_price": str(quote["unit_price"]),
        "total_cost": str(quote["total_cost"]),
        "total_price": str(quote["total_price"]),
        "gross_profit": str(quote["gross_profit"])
    }
