
from langgraph.graph import StateGraph, START, END

from app.workflows.order_state import OrderState
from app.workflows.nodes.extraction_node import extraction_node
from app.workflows.nodes.product_lookup_node import product_lookup_node
from app.workflows.nodes.inventory_node import inventory_node
from app.workflows.nodes.supplier_node import supplier_node
from app.workflows.nodes.planning_node import planning_node
from app.workflows.nodes.policy_node import policy_node
from app.workflows.nodes.policy_enforcement_node import policy_enforcement_node


def route_after_extraction(state: OrderState) -> str:
    if state["status"] == "needs_clarification":
        return "end"

    return "product_lookup"


def route_after_product_lookup(state: OrderState) -> str:
    if state["status"] == "product_found":
        return "inventory"

    return "end"


def build_order_graph():
    # Step 1: Create the graph with shared state.
    builder = StateGraph(OrderState)

    # Step 2: Register all nodes.
    builder.add_node("extraction", extraction_node)
    builder.add_node("product_lookup", product_lookup_node)
    builder.add_node("inventory", inventory_node)
    builder.add_node("supplier", supplier_node)
    builder.add_node("planning", planning_node)
    builder.add_node("policy", policy_node)
    builder.add_node("policy_enforcement", policy_enforcement_node)

    # Step 3: Define the starting point.
    builder.add_edge(START, "extraction")

    # Step 4: Route after extraction.
    builder.add_conditional_edges(
        "extraction",
        route_after_extraction,
        {
            "product_lookup": "product_lookup",
            "end": END
        }
    )

    # Step 5: Route after product lookup.
    builder.add_conditional_edges(
        "product_lookup",
        route_after_product_lookup,
        {
            "inventory": "inventory",
            "end": END
        }
    )

    # Step 6: Connect inventory, planning, and policy nodes.
    builder.add_edge("inventory", "supplier")
    builder.add_edge("supplier", "planning")
    builder.add_edge("planning", "policy")
    builder.add_edge("policy", "policy_enforcement")
    builder.add_edge("policy_enforcement", END)

    # Step 7: Compile the graph.
    return builder.compile()


order_graph = build_order_graph()
