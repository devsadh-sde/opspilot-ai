
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.database.connection import SessionLocal
from app.database.models import OrderProposal
from app.services.order_proposal_service import (
    create_order_proposal,
    review_order_proposal,
)
from app.workflows.order_graph import order_graph


router = APIRouter(
    prefix="/orders",
    tags=["Order Proposals"]
)


class CreateOrderRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ReviewOrderRequest(BaseModel):
    decision: str


# Create a new order proposal
@router.post("/proposals")
def create_proposal(request: CreateOrderRequest):
    result = order_graph.invoke({
        "customer_message": request.message
    })

    if (
        result.get("status") != "ready_for_review"
        or result.get("approval_status") != "pending_human_approval"
    ):
        return {
            "saved": False,
            "analysis": result
        }

    with SessionLocal() as session:
        proposal = create_order_proposal(session, result)

    return {
        "saved": True,
        "proposal": proposal
    }


# List all saved proposals
@router.get("/proposals")
def list_proposals():
    with SessionLocal() as session:
        proposals = session.scalars(
            select(OrderProposal).order_by(
                OrderProposal.created_at.desc(),
                OrderProposal.id.desc()
            )
        ).all()

        return [
            {
                "id": proposal.id,
                "product_id": proposal.product_id,
                "quantity": proposal.quantity,
                "status": proposal.status,
                "created_at": proposal.created_at.isoformat()
            }
            for proposal in proposals
        ]


# Retrieve a specific proposal
@router.get("/proposals/{proposal_id}")
def get_proposal(proposal_id: int):
    with SessionLocal() as session:
        proposal = session.get(OrderProposal, proposal_id)

        if proposal is None:
            raise HTTPException(
                status_code=404,
                detail="Order proposal not found"
            )

        return {
            "id": proposal.id,
            "product_id": proposal.product_id,
            "quantity": proposal.quantity,
            "status": proposal.status,
            "analysis": json.loads(proposal.analysis_json),
            "created_at": proposal.created_at.isoformat()
        }


# Approve or reject a proposal
@router.post("/proposals/{proposal_id}/review")
def review_proposal(
    proposal_id: int,
    request: ReviewOrderRequest
):
    with SessionLocal() as session:
        try:
            return review_order_proposal(
                session=session,
                proposal_id=proposal_id,
                decision=request.decision
            )
        except ValueError as error:
            raise HTTPException(
                status_code=400,
                detail=str(error)
            ) from error
