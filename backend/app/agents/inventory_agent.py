
import json
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from app.tools.inventory_tool import check_inventory
from app.tools.tool_definitions import INVENTORY_TOOL


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def run_inventory_agent(product_id: int) -> str:
    if type(product_id) is not int or product_id <= 0:
        raise ValueError("Product ID must be a positive integer")

    client = Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        timeout=30.0,
        max_retries=0
    )

    message = f"Check available inventory for product ID {product_id}."

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        tools=[INVENTORY_TOOL],
        tool_choice={
            "type": "tool",
            "name": "check_inventory"
        },
        messages=[
            {"role": "user", "content": message}
        ]
    )

    tool_blocks = [
        block for block in response.content
        if block.type == "tool_use"
    ]

    if len(tool_blocks) != 1:
        raise ValueError("Expected one inventory tool request")

    block = tool_blocks[0]

    if block.name != "check_inventory":
        raise ValueError("Unexpected tool requested")

    if block.input != {"product_id": product_id}:
        raise ValueError("Unexpected inventory tool arguments")

    result = check_inventory(product_id=product_id)

    follow_up = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[
            {"role": "user", "content": message},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result)
                }]
            }
        ]
    )

    answers = [
        item.text for item in follow_up.content
        if item.type == "text"
    ]

    return "\n".join(answers)
