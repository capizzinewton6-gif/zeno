"""Language Server Protocol client for deep editor intelligence.

A minimal LSP-style client interface. When a real LSP server is not available,
degrades to the local AST-based analysis. This is a capability module that
provides editor-intelligence primitives to the rest of the agent.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from modeling.ast_manager import ASTManager


@dataclass
class LSPDiagnostic:
    file: str
    line: int
    column: int
    severity: str  # error, warning, info, hint
    message: str
    source: str = ""


@dataclass
class LSPHover:
    file: str
    line: int
    column: int
    content: str


@dataclass
class LSPDefinition:
    file: str
    start_line: int
    end_line: int
    symbol: str


class LSPClient:
    """Minimal LSP client with AST-backed fallbacks."""

    def __init__(self, ast: ASTManager | None = None) -> None:
        self.ast = ast or ASTManager()
        self._servers: dict[str, Any] = {}
        self._symbol_cache: dict[str, dict[str, Any]] = {}

    def start_server(self, language: str) -> bool:
        """Stub for starting an LSP server (not implemented in-process)."""
        self._servers[language] = {"status": "fallback", "engine": "ast"}
        return True

    def stop_server(self, language: str) -> None:
        self._servers.pop(language, None)

    def diagnostics(self, source: str, language: str, file: str = "") -> list[LSPDiagnostic]:
        parsed = self.ast.parse(source, language)
        return [
            LSPDiagnostic(file=file or "<buffer>", line=e_line, column=0,
                          severity="error", message=msg, source="ast")
            for msg, e_line in ((e, 1) for e in parsed.errors)
        ]

    def hover(self, source: str, language: str, line: int, file: str = "") -> LSPHover | None:
        parsed = self.ast.parse(source, language)
        for sym in parsed.symbols:
            if sym.start_line <= line <= sym.end_line:
                content = sym.signature or sym.name
                if sym.docstring:
                    content += f"\n\n{sym.docstring}"
                return LSPHover(file=file, line=line, column=0, content=content)
        return None

    def definition(self, source: str, language: str, name: str, file: str = "") -> LSPDefinition | None:
        parsed = self.ast.parse(source, language)
        for sym in parsed.symbols:
            if sym.name == name:
                return LSPDefinition(file=file, start_line=sym.start_line,
                                     end_line=sym.end_line, symbol=name)
        return None
