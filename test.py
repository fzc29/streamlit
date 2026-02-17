from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

models_to_test = [
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-latest",
]

for model in models_to_test:
    try:
        print(f"Testing {model}...")
        client.messages.create(
            model=model,
            max_tokens=5,
            messages=[{"role": "user", "content": "Hello"}],
        )
        print(f"✅ {model} works\n")
    except Exception as e:
        print(f"❌ {model} not available\n")
