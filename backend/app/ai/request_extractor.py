
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from app.schemas.customer_request import CustomerRequest
from app.services.llm_cost_service import calculate_llm_cost

# Load our API configuration.
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def extract_customer_request(
    customer_message: str,
) -> CustomerRequest:

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is missing")

    client = Anthropic(
        api_key=api_key,
        timeout=30.0,
        max_retries=0,
    )

    response = client.messages.parse(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": customer_message,
            }
        ],
        system=(
            "You extract customer purchase requirements for "
            "Northstar Electronics. Extract the product name, "
            "quantity, delivery deadline, and budget. "
            "Return null for any missing information. "
            "Never invent products, quantities, dates, or budgets. "
            "Do not assume a default quantity."
        ),
        output_format=CustomerRequest,
    )

    if response.parsed_output is None:
        raise ValueError("No structured request returned")

    # Track token consumption for this Claude request.
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    # Calculate the cost of this Claude request.
    estimated_cost = calculate_llm_cost(
        input_tokens = input_tokens,
        output_tokens = output_tokens
    )

    print("\n--- Claude API Usage ---")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Total tokens: {input_tokens + output_tokens}")
    print(f"Estimated cost: ${estimated_cost:.6f}")
    
    return response.parsed_output
