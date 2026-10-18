
INVENTORY_TOOL = {
    "name": "check_inventory",
    "description": (
        "Check available warehouse inventory for a product "
        "using its product ID. Returns stock quantities "
        "for each warehouse and total available stock."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "product_id": {
                "type": "integer",
                "description": "The product ID to check."
            }
        },
        "required": ["product_id"],
        "additionalProperties": False
    }
}


SUPPLIER_TOOL = {
    "name": "check_suppliers",
    "description": (
        "Retrieve supplier offers for a product using its "
        "product ID. Returns available quantities, unit costs, "
        "and estimated lead times."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "product_id": {
                "type": "integer",
                "description": "The product ID to check supplier offers for.",
                "minimum": 1
            }
        },
        "required": ["product_id"],
        "additionalProperties": False
    }
}
