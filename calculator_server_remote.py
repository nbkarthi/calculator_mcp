"""
Calculator MCP for Railway (or any host that sets PORT).

Start command example: uv run python calculator_server_remote.py

MCP endpoint (default): /mcp  (streamable-http)
Optional: MCP_TRANSPORT=sse for SSE transport instead.
"""

import os
import sys
from typing import Literal

from mcp.server import FastMCP
from starlette.responses import JSONResponse

_host = "0.0.0.0"
_port = int(os.environ.get("PORT", "8000"))
_raw = (os.environ.get("MCP_TRANSPORT") or "streamable-http").lower().strip()
if _raw == "sse":
    _transport: Literal["sse", "streamable-http"] = "sse"
else:
    if _raw != "streamable-http":
        print(
            f"MCP_TRANSPORT must be 'sse' or 'streamable-http', got {_raw!r}; using streamable-http",
            file=sys.stderr,
        )
    _transport = "streamable-http"

mcp = FastMCP("Calculator Server", host=_host, port=_port)


@mcp.custom_route("/health", methods=["GET"])
async def health(_request):
    return JSONResponse({"status": "ok", "service": "calculator-mcp"})


@mcp.tool(description="Add two numbers together")
def add(x: float, y: float) -> float:
    """Add two numbers and return the result."""
    return x + y


@mcp.tool(description="Subtract second number from first number")
def subtract(x: float, y: float) -> float:
    """Subtract y from x and return the result."""
    return x - y


@mcp.tool(description="Multiply two numbers together")
def multiply(x: float, y: float) -> float:
    """Multiply two numbers and return the result."""
    return x * y


@mcp.tool(description="Divide first number by second number")
def divide(x: float, y: float) -> float:
    """Divide x by y and return the result."""
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y


if __name__ == "__main__":
    print(
        f"Starting Calculator MCP Server ({_transport} on {_host}:{_port})...",
        file=sys.stderr,
    )
    mcp.run(transport=_transport)
