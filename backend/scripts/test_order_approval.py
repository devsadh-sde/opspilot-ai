
from app.database.connection import SessionLocal
from app.services.order_proposal_service import (
    create_order_proposal,
    review_order_proposal,
)


def create_test_proposal(session):
    # Create a valid proposal for testing.
    graph_result = {
        "status": "ready_for_review",
        "approval_status": "pending_human_approval",
        "product_id": 1,
        "quantity": 10,
        "order_analysis": {
            "status": "ready_for_review",
            "fulfillment": {
                "allocated_quantity": 10,
                "unfulfilled_quantity": 0
            },
            "pricing": {
                "total_price": "15000.00",
                "within_budget": True
            }
        }
    }

    return create_order_proposal(session, graph_result)


def main():
    with SessionLocal() as session:

        # Test 1: Approve a pending proposal.
        proposal = create_test_proposal(session)

        approved = review_order_proposal(
            session=session,
            proposal_id=proposal["id"],
            decision="approve"
        )

        assert approved["status"] == "approved"
        print("Test 1 passed: Proposal approved")

        # Test 2: Reject a different proposal.
        proposal = create_test_proposal(session)

        rejected = review_order_proposal(
            session=session,
            proposal_id=proposal["id"],
            decision="reject"
        )

        assert rejected["status"] == "rejected"
        print("Test 2 passed: Proposal rejected")

        # Test 3: Prevent reviewing twice.
        try:
            review_order_proposal(
                session=session,
                proposal_id=proposal["id"],
                decision="approve"
            )
        except ValueError as error:
            assert "Cannot review" in str(error)
            print("Test 3 passed: Duplicate review blocked")
        else:
            raise AssertionError(
                "Duplicate review should have failed"
            )

    print("\nAll human approval tests passed!")


if __name__ == "__main__":
    main()
