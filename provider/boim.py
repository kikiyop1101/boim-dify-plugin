from typing import Any

from dify_plugin import ToolProvider


class BoimProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # BOIM is a public read-only service: there are no credentials to validate.
        return None
