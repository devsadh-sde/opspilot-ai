
from typing import TypedDict


class OrderState(TypedDict, total=False):
    # Customer request
    customer_message: str
    product_name: str
    product_id: int
    quantity: int
    budget: str | None
    deadline: str | None

    # Workflow control
    status: str
    question: str | None

    # Agent/tool results
    inventory: dict
    suppliers: dict

    # Planning results
    order_analysis: dict

    # Policy RAG results
    policies: list[dict]

    # Human approval
    approval_status: str

    policy_evaluation: dict
