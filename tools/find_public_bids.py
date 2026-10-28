from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from boim_client import call_tool, join, summarize


def describe(item: dict[str, Any]) -> str:
    price = item.get("estimated_price_krw")
    return join([
        item.get("title"),
        item.get("type"),
        item.get("agency"),
        item.get("region"),
        "deadline " + item["deadline"].replace("T", " ")[:16] + " KST" if item.get("deadline") else None,
        f"estimated price KRW {price:,}" if isinstance(price, int) else None,
        item.get("contract_method"),
        item.get("award_method"),
        item.get("notice"),
        f"source: {item['origin']}" if item.get("origin") else None,
    ])


class FindPublicBidsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        result = call_tool("find_public_bids", {
            "region": tool_parameters.get("region"),
            "category": tool_parameters.get("category"),
            "type": tool_parameters.get("bid_type"),
            "query": tool_parameters.get("query"),
        })
        yield self.create_text_message(summarize(result, describe))
        yield self.create_json_message(result)
