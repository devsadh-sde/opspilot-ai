
import json

from sqlalchemy.orm import Session

from app.database.models import OrderProposal


def create_order_proposal(
    session: Session,
    graph_result: dict
) -> dict:
    # Step 1: Validate the workflow result.
    if graph_result.get("status") != "ready_for_review":
        raise ValueError(
            "Only orders ready for review can become proposals"
        )

    if graph_result.get("approval_status") != "pending_human_approval":
        raise ValueError(
            "Order has unresolved approval requirements"
        )

    if "order_analysis" not in graph_result:
        raise ValueError("Missing order analysis")

    # Step 2: Create the database record.
    proposal = OrderProposal(
        product_id=graph_result["product_id"],
        quantity=graph_result["quantity"],
        status="pending_review",
        analysis_json=json.dumps(graph_result)
    )

    # Step 3: Save to SQLite.
    session.add(proposal)
    session.commit()
    session.refresh(proposal)

    # Step 4: Return the saved proposal.
    return {
        "id": proposal.id,
        "product_id": proposal.product_id,
        "quantity": proposal.quantity,
        "status": proposal.status,
        "created_at": proposal.created_at.isoformat()
    }


def review_order_proposal(
    session: Session,
    proposal_id: int,
    decision: str
) -> dict:
    # Step 1: Validate inputs.
    if type(proposal_id) is not int or proposal_id <= 0:
        raise ValueError("Proposal ID must be a positive integer")

    if decision not in ("approve", "reject"):
        raise ValueError("Decision must be 'approve' or 'reject'")

    # Step 2: Retrieve the saved proposal.
    proposal = session.get(OrderProposal, proposal_id)

    if proposal is None:
        raise ValueError("Order proposal not found")

    # Step 3: Prevent reviewing the same proposal twice.
    if proposal.status != "pending_review":
        raise ValueError(
            f"Cannot review a proposal with status '{proposal.status}'"
        )

    # Step 4: Verify the saved analysis before approving.
    if decision == "approve":
        analysis = json.loads(proposal.analysis_json)

        if (
            analysis.get("status") != "ready_for_review"
            or analysis.get("approval_status") != "pending_human_approval"
        ):
            raise ValueError(
                "Proposal has unresolved approval requirements"
            )

    # Step 5: Update the review status.
    proposal.status = (
        "approved" if decision == "approve" else "rejected"
    )

    session.commit()
    session.refresh(proposal)

    return {
        "id": proposal.id,
        "status": proposal.status,
        "product_id": proposal.product_id,
        "quantity": proposal.quantity
    }
