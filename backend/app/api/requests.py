
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.workflows.order_graph import order_graph


router = APIRouter()


class AnalyzeRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


@router.post("/requests/analyze")
def analyze_customer_request(request: AnalyzeRequest):
    result = order_graph.invoke({
        "customer_message": request.message
    })

    return result
