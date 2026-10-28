"""Client for BOIM's public MCP endpoint (https://boim.io/api/mcp): read-only, no API key.

Every tool sends one JSON-RPC `tools/call` request to that fixed URL and returns
BOIM's structured result unchanged, plus a short text summary for the model.
"""

from collections.abc import Callable
from typing import Any

import httpx

MCP_URL = "https://boim.io/api/mcp"
USER_AGENT = "boim-dify-plugin/0.0.1"
TIMEOUT_SECONDS = 20
MAX_ARGUMENT_CHARS = 100
RESULT_LIMIT = 5  # BOIM returns up to 5 results per call without a key; the rest is linked in `more`


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Call one BOIM MCP tool and return its structuredContent."""
    args: dict[str, Any] = {
        key: str(value).strip()[:MAX_ARGUMENT_CHARS]
        for key, value in arguments.items()
        if value is not None and str(value).strip()
    }
    args["limit"] = RESULT_LIMIT
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": args}}
    try:
        response = httpx.post(
            MCP_URL,
            json=payload,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json, text/event-stream"},
            timeout=TIMEOUT_SECONDS,
        )
    except httpx.HTTPError as error:
        raise RuntimeError(f"BOIM (boim.io) could not be reached: {type(error).__name__}. Please try again shortly.") from None
    if response.status_code in (403, 429):
        raise RuntimeError("BOIM (boim.io) is limiting requests right now. Please wait a few minutes and try again.")
    if response.status_code != 200:
        raise RuntimeError(f"BOIM (boim.io) returned HTTP {response.status_code}. Please try again later.")
    try:
        message = response.json()
    except ValueError:
        raise RuntimeError("BOIM (boim.io) returned an unexpected response. Please try again later.") from None
    if message.get("error"):
        raise RuntimeError(f"BOIM (boim.io) error: {message['error'].get('message', 'unknown error')}")
    result = message.get("result") or {}
    if result.get("isError"):
        texts = [part.get("text", "") for part in result.get("content") or [] if part.get("type") == "text"]
        raise RuntimeError("BOIM (boim.io) could not run this search: " + (" ".join(texts) or "unknown error"))
    return result.get("structuredContent") or {}


def summarize(result: dict[str, Any], describe: Callable[[dict[str, Any]], str]) -> str:
    """One line per result with its BOIM or original URL, then counts, notes and the citation line."""
    head = f"BOIM (boim.io): {result.get('total', 0)} found, {result.get('shown', 0)} shown."
    if result.get("order"):
        head += f" Order: {result['order']}"
    lines = [head]
    for item in result.get("results") or []:
        url = item.get("card") or item.get("url") or item.get("list_page") or ""
        lines.append(f"- {describe(item)} | {url}")
    if result.get("not_shown"):
        lines.append(f"{result['not_shown']} more in the full list: {result.get('more', '')}")
    for key in ("note", "limits"):
        if result.get(key):
            lines.append(f"Note: {result[key]}")
    lines.append(result.get("cite") or f"Source: {result.get('source') or 'BOIM (boim.io)'}")
    return "\n".join(lines)


def join(parts: list[Any]) -> str:
    return " · ".join(str(part) for part in parts if part)
