"""Rich terminal components, progress bars, and syntax highlighting.

Uses the ``rich`` library when available; falls back to plain text otherwise.
"""
from __future__ import annotations

import sys
from typing import Any, Iterable

try:  # pragma: no cover - optional
    from rich.console import Console
    from rich.syntax import Syntax
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.table import Table
    from rich.panel import Panel
    _RICH = True
except Exception:  # pragma: no cover
    _RICH = False


class TerminalUI:
    """Rich-powered terminal rendering with plain-text fallback."""

    def __init__(self) -> None:
        self._console = Console() if _RICH else None

    def code(self, source: str, language: str = "python") -> str:
        if _RICH:
            syntax = Syntax(source, language, theme="monokai", line_numbers=True)
            self._console.print(syntax)
            return source
        print(source)
        return source

    def panel(self, title: str, content: str) -> None:
        if _RICH:
            self._console.print(Panel(content, title=title))
        else:
            print(f"== {title} ==\n{content}")

    def table(self, headers: list[str], rows: list[list[str]], title: str = "") -> None:
        if _RICH:
            t = Table(title=title)
            for h in headers:
                t.add_column(h)
            for row in rows:
                t.add_row(*row)
            self._console.print(t)
        else:
            print(f"\n{title}".strip())
            print(" | ".join(headers))
            print("-" * 40)
            for row in rows:
                print(" | ".join(row))

    def progress(self, iterable: Iterable, description: str = "Working") -> Iterable:
        items = list(iterable)
        if _RICH:
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                          BarColumn(), TextColumn("{task.completed}/{task.total}")) as prog:
                task = prog.add_task(description, total=len(items))
                for item in items:
                    yield item
                    prog.update(task, advance=1)
        else:
            for i, item in enumerate(items, 1):
                print(f"{description}... {i}/{len(items)}")
                yield item

    def info(self, message: str) -> None:
        if _RICH:
            self._console.print(f"[cyan]ℹ[/cyan] {message}")
        else:
            print(f"[INFO] {message}")

    def success(self, message: str) -> None:
        if _RICH:
            self._console.print(f"[green]✓[/green] {message}")
        else:
            print(f"[OK] {message}")

    def warning(self, message: str) -> None:
        if _RICH:
            self._console.print(f"[yellow]⚠[/yellow] {message}")
        else:
            print(f"[WARN] {message}")

    def error(self, message: str) -> None:
        if _RICH:
            self._console.print(f"[red]✗[/red] {message}")
        else:
            print(f"[ERROR] {message}", file=sys.stderr)
