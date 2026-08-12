"""Tree-sitter and AST parsing/transformation pipeline.

Wraps tree-sitter (when available) and Python's ``ast`` module to provide a
uniform interface for parsing, querying, and transforming source code across
languages. Falls back gracefully when tree-sitter is not installed.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Any

try:  # pragma: no cover - optional dependency
    import tree_sitter as ts  # type: ignore
    from tree_sitter_languages import get_parser  # type: ignore

    _TS_AVAILABLE = True
except Exception:  # pragma: no cover
    ts = None  # type: ignore
    get_parser = None  # type: ignore
    _TS_AVAILABLE = False


@dataclass
class Symbol:
    name: str
    kind: str  # function, class, method, variable, import
    start_line: int
    end_line: int
    language: str
    signature: str = ""
    docstring: str = ""
    children: list[str] = field(default_factory=list)


@dataclass
class ParseResult:
    language: str
    source: str
    symbols: list[Symbol] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


class ASTManager:
    """Unified AST access layer."""

    SUPPORTED = {
        "python", "javascript", "typescript", "rust", "go", "cpp",
        "c", "java", "kotlin", "bash", "html", "sql",
    }

    def parse(self, source: str, language: str) -> ParseResult:
        if language.lower() == "python":
            return self._parse_python(source)
        if _TS_AVAILABLE:
            return self._parse_treesitter(source, language)
        return ParseResult(language=language, source=source,
                           errors=["tree-sitter not installed"])

    # -- Python via stdlib ast ------------------------------------------------
    def _parse_python(self, source: str) -> ParseResult:
        symbols: list[Symbol] = []
        errors: list[str] = []
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            return ParseResult("python", source, errors=[f"{exc.msg} (line {exc.lineno})"])

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                symbols.append(Symbol(
                    name=node.name, kind="function",
                    start_line=node.lineno, end_line=node.end_lineno or node.lineno,
                    language="python", signature=self._py_sig(node),
                    docstring=ast.get_docstring(node) or "",
                ))
            elif isinstance(node, ast.ClassDef):
                members = [n.name for n in node.body
                           if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                symbols.append(Symbol(
                    name=node.name, kind="class",
                    start_line=node.lineno, end_line=node.end_lineno or node.lineno,
                    language="python", docstring=ast.get_docstring(node) or "",
                    children=members,
                ))
        return ParseResult("python", source, symbols=symbols, errors=errors)

    def _py_sig(self, node: ast.FunctionDef) -> str:
        args = [a.arg for a in node.args.args]
        returns = ast.unparse(node.returns) if node.returns else ""
        ret = f" -> {returns}" if returns else ""
        return f"{node.name}({', '.join(args)}){ret}"

    # -- Other languages via tree-sitter -------------------------------------
    def _parse_treesitter(self, source: str, language: str) -> ParseResult:  # pragma: no cover
        try:
            parser = get_parser(language)
            tree = parser.parse(bytes(source, "utf8"))
            symbols = self._extract_symbols(tree.root_node, language)
            return ParseResult(language, source, symbols=symbols)
        except Exception as exc:
            return ParseResult(language, source, errors=[str(exc)])

    def _extract_symbols(self, node, language: str) -> list[Symbol]:  # pragma: no cover
        kinds = {"function_definition": "function", "class_declaration": "class",
                 "method_declaration": "method", "function_declaration": "function"}
        out: list[Symbol] = []
        stack = [node]
        while stack:
            n = stack.pop()
            if n.type in kinds:
                name_node = n.child_by_field_name("name")
                name = name_node.text.decode() if name_node and name_node.text else "<anon>"
                out.append(Symbol(
                    name=name, kind=kinds[n.type],
                    start_line=n.start_point[0] + 1, end_line=n.end_point[0] + 1,
                    language=language,
                ))
            stack.extend(n.children)
        return out

    # -- Transformation ------------------------------------------------------
    def list_functions(self, source: str, language: str = "python") -> list[str]:
        result = self.parse(source, language)
        return [s.name for s in result.symbols if s.kind == "function"]

    def extract_function(self, source: str, name: str,
                         language: str = "python") -> str | None:
        result = self.parse(source, language)
        for sym in result.symbols:
            if sym.name == name:
                lines = source.splitlines()
                return "\n".join(lines[sym.start_line - 1: sym.end_line])
        return None
