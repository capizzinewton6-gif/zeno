"""Captures linter warnings, syntax errors, and compiler hints."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from lsp_integration.lsp_client import LSPClient, LSPDiagnostic
from modeling.ast_manager import ASTManager


@dataclass
class DiagnosticBatch:
    errors: list[LSPDiagnostic] = field(default_factory=list)
    warnings: list[LSPDiagnostic] = field(default_factory=list)
    infos: list[LSPDiagnostic] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.errors) + len(self.warnings) + len(self.infos)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)


class DiagnosticsHandler:
    """Aggregates diagnostics from the LSP client and language engines."""

    def __init__(self, client: LSPClient | None = None) -> None:
        self.client = client or LSPClient()

    def collect(self, source: str, language: str, file: str = "") -> DiagnosticBatch:
        diags = self.client.diagnostics(source, language, file)
        batch = DiagnosticBatch()
        for d in diags:
            if d.severity == "error":
                batch.errors.append(d)
            elif d.severity == "warning":
                batch.warnings.append(d)
            else:
                batch.infos.append(d)
        return batch

    def summarize(self, batch: DiagnosticBatch) -> str:
        parts = [f"{len(batch.errors)} errors", f"{len(batch.warnings)} warnings",
                 f"{len(batch.infos)} infos"]
        return ", ".join(parts)

    def to_quickfix(self, batch: DiagnosticBatch) -> list[dict[str, Any]]:
        """Emit quickfix-style entries for editor integration."""
        out: list[dict[str, Any]] = []
        for d in [*batch.errors, *batch.warnings, *batch.infos]:
            out.append({"file": d.file, "line": d.line, "col": d.column,
                        "severity": d.severity, "text": d.message})
        return out
