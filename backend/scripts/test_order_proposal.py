
from app.database.connection import SessionLocal
from app.database.models import OrderProposal
from app.services.order_proposal_service import create_order_proposal


def main():
    # Sample result matching our LangGraph output.
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

    with SessionLocal() as session:
        result = create_order_proposal(
            session=session,
            graph_result=graph_result
        )

        print("\n--- Saved Order Proposal ---")
        print(result)

        assert result["id"] > 0
        assert result["product_id"] == 1
        assert result["quantity"] == 10
        assert result["status"] == "pending_review"

        # Verify that the record actually exists in SQLite.
        saved_proposal = session.get(
            OrderProposal,
            result["id"]
        )

        assert saved_proposal is not None
        assert saved_proposal.status == "pending_review"

        print("\nAll order proposal tests passed!")


if __name__ == "__main__":
    main()
