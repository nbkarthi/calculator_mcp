import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.models.openai import OpenAIModel
from strands.tools.mcp import MCPClient

ROOT = Path(__file__).resolve().parent


def main() -> None:
    load_dotenv(ROOT / ".env")
    key = os.environ.get("OPENAI_API_KEY","TEST")
    if not key:
        sys.exit("Missing OPENAI_API_KEY (set in .env or the environment).")

    mcp = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(
                command=sys.executable,
                args=[str(ROOT / "calculator_server.py")],
                cwd=str(ROOT),
            )
        )
    )

    agent = Agent(
        model=OpenAIModel(
            client_args={"api_key": key},
            model_id=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        ),
        tools=[mcp],
        system_prompt="Use the calculator MCP tools for arithmetic.",
    )

    prompt = os.environ.get("CALCULATOR_PROMPT", "What is 847 × 23? Use the tools.")
    print(agent(prompt))


if __name__ == "__main__":
    main()
