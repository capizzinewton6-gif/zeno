"""Type definitions and symbol location resolver."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from lsp_integration.lsp_client import LSPClient, LSPDefinition


@dataclass
class TypeDefinition:
    name: str
    file: str
    line: int
    type_kind: str  # class, function, variable, alias


class DefinitionProvider:
    """Resolves go-to-definition requests via the LSP client."""

    def __init__(self, client: LSPClient | None = None) -> None:
        self.client = client or LSPClient()

    def resolve(self, source: str, language: str, symbol: str,
                file: str = "") -> LSPDefinition | None:
        return self.client.definition(source, language, symbol, file)

    def resolve_all(self, source: str, language: str,
                    symbols: list[str], file: str = "") -> list[LSPDefinition]:
        out: list[LSPDefinition] = []
        for sym in symbols:
            d = self.resolve(source, language, sym, file)
            if d:
                out.append(d)
        return out

    def type_definition(self, source: str, language: str, symbol: str,
                        file: str = "") -> TypeDefinition | None:
        d = self.resolve(source, language, symbol, file)
        if not d:
            return None
        return TypeDefinition(name=symbol, file=d.file, line=d.start_line, type_kind="class")
