import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

#Loaad configuration from .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# Get the API key from environment variables
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("Please configure your ANTHROPIC_API_KEY.")

# Initialize the Anthropic client
client = Anthropic(
    api_key=api_key,
    timeout=30.0,
    max_retries=0,
)

#Send request to Claude API
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Say hello to this project."
        }
    ]
)

# Print the response from the Claude API
for block in response.content:
    if block.type == "text":
        print("Claude:",block.text)

print("Input tokens:", response.usage.input_tokens)
print("Output tokens:", response.usage.output_tokens)

 