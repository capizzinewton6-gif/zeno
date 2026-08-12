"""Hover documentation and signature helper."""
from __future__ import annotations

from typing import Any

from lsp_integration.lsp_client import LSPClient, LSPHover


class HoverProvider:
    """Provides hover information for symbols under the cursor."""

    def __init__(self, client: LSPClient | None = None) -> None:
        self.client = client or LSPClient()

    def hover(self, source: str, language: str, line: int,
              file: str = "") -> LSPHover | None:
        return self.client.hover(source, language, line, file)

    def signature_help(self, source: str, language: str, symbol: str,
                       file: str = "") -> str | None:
        d = self.client.definition(source, language, symbol, file)
        if not d:
            return None
        hov = self.client.hover(source, language, d.start_line, file)
        return hov.content if hov else None

    def markdown_hover(self, source: str, language: str, line: int,
                       file: str = "") -> str | None:
        hov = self.hover(source, language, line, file)
        if not hov:
            return None
        return f"```{language}\n{hov.content}\n```"
