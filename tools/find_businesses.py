from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from boim_client import call_tool, join, summarize


def describe(item: dict[str, Any]) -> str:
    return join([
        item.get("name"),
        item.get("category"),
        item.get("area"),
        "registered on BOIM by the business" if item.get("registered") else None,
        f"food business permit {item['license_year']}" if item.get("license_year") else None,
    ])


class FindBusinessesTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        result = call_tool("find_businesses", {
            "region": tool_parameters.get("region"),
            "category": tool_parameters.get("category"),
            "query": tool_parameters.get("query"),
        })
        yield self.create_text_message(summarize(result, describe))
        yield self.create_json_message(result)
