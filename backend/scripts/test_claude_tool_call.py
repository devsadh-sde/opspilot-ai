import json
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from app.tools.tool_definitions import INVENTORY_TOOL
from app.tools.inventory_tool import check_inventory

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    timeout=30.0,
    max_retries=0
)

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=300,
    tools=[INVENTORY_TOOL],
    messages=[
        {
            "role": "user",
            "content": (
                "Check the available inventory for product ID 1."
            )
        }
    ]
)

print("\n--- Claude Response ---")
print("Stop reason:", response.stop_reason)

for block in response.content:
    print("Block type:", block.type)

    if block.type == "tool_use":
            if block.name == "check_inventory":
                result = check_inventory(
                    product_id=block.input["product_id"]
                )

                print("\n--- Actual Database Result ---")
                print(result)

            follow_up = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                tools=[INVENTORY_TOOL],
                messages=[
                    {
                        "role": "user",
                        "content": "Check the available inventory for product ID 1."
                    },
                    {
                        "role": "assistant",
                        "content": response.content
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps(result)
                            }
                        ]
                    }
                ]
            )

            print("\n--- Claude Final Answer ---")
            for item in follow_up.content:
                if item.type == "text":
                    print(item.text)
    print("Tool name:", block.name)
    print("Tool input:", block.input)
    print("Tool use ID:", block.id)