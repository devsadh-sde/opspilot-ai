
from decimal import Decimal


def calculate_llm_cost(
    input_tokens: int,
    output_tokens: int
) -> Decimal:

    # Claude Haiku 4.5 standard pricing per million tokens
    input_rate = Decimal("1.00")
    output_rate = Decimal("5.00")

    million = Decimal("1000000")

    input_cost = (
        Decimal(input_tokens) * input_rate / million
    )

    output_cost = (
        Decimal(output_tokens) * output_rate / million
    )

    return input_cost + output_cost
