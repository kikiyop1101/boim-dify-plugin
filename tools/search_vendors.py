from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from boim_client import call_tool, join, summarize


def describe(item: dict[str, Any]) -> str:
    items = item.get("categories") or []
    deliveries = item.get("procurement_1y") or {}
    registered = item.get("registered_by_vendor") or {}
    return join([
        item.get("name"),
        item.get("region"),
        f"region match: {item['match']}" if item.get("match") else None,
        ("items: " + ", ".join(items[:6]) + (" …" if len(items) > 6 else "")) if items else None,
        item.get("business_status"),
        f"public deliveries in 12 months: {deliveries['records']} to {deliveries.get('agencies', 0)} agencies"
        if deliveries.get("records") else None,
        ("tags: " + ", ".join(item["tags"][:5])) if item.get("tags") else None,
        f"service area: {registered['service_area']}" if registered.get("service_area") else None,
        f"phone: {registered['phone']}" if registered.get("phone") else None,
        f"website: {registered['website']}" if registered.get("website") else None,
        f"price: {registered['price_note']}" if registered.get("price_note") else None,
    ])


class SearchVendorsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        result = call_tool("search_vendors", {
            "category": tool_parameters.get("category"),
            "region": tool_parameters.get("region"),
            "query": tool_parameters.get("query"),
            "cert": tool_parameters.get("cert"),
        })
        yield self.create_text_message(summarize(result, describe))
        yield self.create_json_message(result)
