#!/usr/bin/env python3
"""Holographic UI - text/ANSI front-end for the Tony Stark Hologram OS."""

from __future__ import annotations

import os
import sys
import time
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.text import Text

    _CONSOLE = Console()
    _HAS_RICH = True
except ImportError:  # pragma: no cover - rich is a declared dependency
    _CONSOLE = None
    _HAS_RICH = False


_ARC = r"""
        .  . *  .   *   .     *    .    *   .
      *   .    .  *   .    *   .   .   *    .
    .   *   .   (  ARC REACTOR  )   .   *   .
      *   .    .  *   .    *   .   .   *    .
        .  *  .   *   .     *    .    *   .
"""


class HolographicUI:
    """Cyan-tinted, panel-wrapped console output + REPL."""

    CYAN = "bright_cyan"
    AMBER = "yellow"
    GREEN = "green"

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    # -- low level helpers --------------------------------------------------
    def _emit(self, text: str, style: Optional[str] = None):
        if _HAS_RICH:
            _CONSOLE.print(text, style=style)
        else:
            print(text)

    def panel(self, body: str, title: str = "J.A.R.V.I.S.", style: Optional[str] = None):
        if _HAS_RICH:
            _CONSOLE.print(Panel.fit(body, title=title, border_style=style or self.CYAN))
        else:
            print(f"\n--- {title} ---\n{body}\n")

    def speak(self, text: str):
        """Voice-style line (rendered as quoted, stylised text)."""
        self._emit(f'\u201c{text}\u201d', self.GREEN)

    def banner(self, text: str):
        self._emit(text, self.CYAN)

    def warn(self, text: str):
        self._emit(f"[!] {text}", self.AMBER)

    # -- animation pieces ---------------------------------------------------
    def arc_reactor(self):
        self._emit(_ARC, self.CYAN)

    def progress(self, label: str, total: int = 100, sleep: float = 0.01):
        if _HAS_RICH:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("{task.percentage:>3.0f}%"),
                console=_CONSOLE,
                transient=False,
            ) as prog:
                task = prog.add_task(label, total=total)
                for i in range(total):
                    prog.update(task, advance=1)
                    time.sleep(sleep)
        else:
            sys.stdout.write(f"{label}: ")
            for i in range(total):
                sys.stdout.write("#" if i % 10 == 0 else ".")
                sys.stdout.flush()
                time.sleep(sleep)
            sys.stdout.write(" done\n")

    def grid(self):
        """Render a holographic floor grid."""
        lines = []
        for i in range(7):
            line = "  " + "   ".join(f"{(i*7+j)%10}" for j in range(23))
            lines.append(line)
        grid_txt = "\n".join(lines)
        self.panel(grid_txt, title="SPATIAL GRID", style=self.CYAN)

    # -- REPL ----------------------------------------------------------------
    def run_workspace(self, workspace):
        self.banner("=" * 60)
        self.banner("  TONY STARK HOLOGRAM OS - WORKSPACE ONLINE")
        self.banner("  Type 'help' for commands, 'exit' to power down.")
        self.banner("=" * 60)
        while True:
            try:
                cmd = input("\nholo> ").strip()
            except (EOFError, KeyboardInterrupt):
                self.banner("\n[power] hologram offline.")
                break
            if not cmd:
                continue
            if cmd.lower() in ("exit", "quit", "power down"):
                self.speak("Powering down. Goodbye, Operator.")
                break
            result = workspace.execute(cmd)
            if isinstance(result, dict):
                self.panel(
                    "\n".join(f"{k}: {v}" for k, v in result.items()),
                    title="RESULT",
                    style=self.CYAN,
                )
            else:
                self.speak(str(result))
