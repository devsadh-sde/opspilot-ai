
from app.agents.inventory_agent import run_inventory_agent
from app.agents.supplier_agent import run_supplier_agent


def analyze_fulfillment(product_id: int) -> dict:
    if type(product_id) is not int or product_id <= 0:
        raise ValueError("Product ID must be a positive integer")

    inventory_analysis = run_inventory_agent(product_id)
    supplier_analysis = run_supplier_agent(product_id)

    return {
        "product_id": product_id,
        "inventory_analysis": inventory_analysis,
        "supplier_analysis": supplier_analysis
    }
