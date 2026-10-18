
from app.tools.inventory_tool import check_inventory
from app.tools.supplier_tool import check_suppliers


def create_fulfillment_plan(product_id: int, quantity: int) -> dict:
    if type(product_id) is not int or product_id <= 0:
        raise ValueError("Product ID must be a positive integer")

    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Quantity must be a positive integer")

    inventory = check_inventory(product_id)
    supplier_data = check_suppliers(product_id)

    remaining = quantity
    allocations = []

    # Allocate existing warehouse stock first.
    for warehouse in inventory["warehouses"]:
        allocated = min(remaining, warehouse["quantity"])

        if allocated > 0:
            allocations.append({
                "source": "warehouse",
                "source_id": warehouse["warehouse_id"],
                "quantity": allocated
            })
            remaining -= allocated

    # Use supplier availability for any shortage.
    for supplier in supplier_data["suppliers"]:
        if remaining == 0:
            break

        allocated = min(remaining, supplier["available_quantity"])

        if allocated > 0:
            allocations.append({
                "source": "supplier",
                "source_id": supplier["supplier_id"],
                "quantity": allocated,
                "unit_cost": supplier["unit_cost"],
                "lead_time_days": supplier["lead_time_days"]
            })
            remaining -= allocated

    return {
        "product_id": product_id,
        "requested_quantity": quantity,
        "allocated_quantity": quantity - remaining,
        "unfulfilled_quantity": remaining,
        "status": "feasible" if remaining == 0 else "insufficient_stock",
        "allocations": allocations
    }
