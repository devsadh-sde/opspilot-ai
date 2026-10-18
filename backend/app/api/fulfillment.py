
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.workflows.fulfillment_workflow import analyze_fulfillment


router = APIRouter(prefix="/fulfillment", tags=["Fulfillment"])


class FulfillmentRequest(BaseModel):
    product_id: int = Field(gt=0, strict=True)


@router.post("/analyze")
def analyze_fulfillment_request(request: FulfillmentRequest):
    result = analyze_fulfillment(
        product_id=request.product_id
    )

    return result
