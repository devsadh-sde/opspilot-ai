
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.workflows.request_workflow import (
    process_customer_request,
)


router = APIRouter()


class AnalyzeRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000
    )


@router.post("/requests/analyze")
def analyze_request(request: AnalyzeRequest):
    return process_customer_request(
        request.message
    )
