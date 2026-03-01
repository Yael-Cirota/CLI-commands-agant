import os
import ssl
import truststore
import httpx
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Use Windows system certificate store to fix SSL inspection by security software
_ssl_ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
_http_client = httpx.Client(verify=_ssl_ctx)

load_dotenv(Path(__file__).parent / ".env")

# Load level-1 prompt directly as plain text
PROMPT_PATH = Path(__file__).parent / "prompts" / "level-1.md"
SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8").strip()

def natural_to_cli(user_input: str) -> str:
    """Convert a natural language instruction to a Windows CLI command."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is not set. Add it to the .env file.")
    client = OpenAI(api_key=key, http_client=_http_client)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        temperature=0,
        max_tokens=256,
    )
    return response.choices[0].message.content.strip()


def main():
    print("Windows CLI Command Generator — type 'exit' to quit\n")
    while True:
        user_input = input("Instruction: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue
        result = natural_to_cli(user_input)
        print(f"Command: {result}\n")


if __name__ == "__main__":
    main()

