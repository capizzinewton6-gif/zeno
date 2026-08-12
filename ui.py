"""Text-GUI for Zeno, the autonomous AI Physics Assistant.

Built on Rich. Provides an interactive REPL with first-class rendering of
simulation results: every simulation produces a matplotlib figure that is saved
to ``plots/`` AND rendered inline in the terminal (as a sixel/inline image when
the terminal supports it, otherwise as an ASCII preview). This is where all
simulations are visualised, per the design requirement.

Commands:
  solve <problem>      Decompose & reason through a physics problem
  explain <concept>    Plain-language explanation of a concept
  simulate <name>      Run a simulation and render it in the UI
  sims                  List available simulations
  verify k=v ...       Run physical-safety checks (mass=.. speed=.. etc.)
  lit <query>          Search the literature (offline canonical refs)
  constants            Print the CODATA fundamental constants table
  clear                Clear the screen
  help                  Show this help
  quit                  Exit
"""

from __future__ import annotations

import os
import shlex
import sys
import traceback
from pathlib import Path
from typing import Callable

import numpy as np
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from agents.physics_agent import PHYSICS_AGENT
from agents.compute_agent import ComputeAgent
from tools.constant_engine import CONSTANTS
from tools.plot_generator import PLOTTER


_HERE = Path(__file__).resolve().parent
_PLOTS_DIR = _HERE / "plots"
_PLOTS_DIR.mkdir(exist_ok=True)


BANNER = r"""
███████╗██╗██████╗  ██████╗ ███╗   ██╗
╚══███╔╝██║██╔══██╗██╔═══╝ ████╗  ██║
  ███╔╝ ██║██████╔╝██║  ███╗██╔██╗ ██║
 ███╔╝  ██║██╔══██╗██║   ██║██║╚██╗██║
███████╗██║██████╔╝╚██████╔╝██║ ╚████║
╚══════╝╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
   Autonomous AI Physics Assistant & Virtual Laboratory
"""


class ZenoUI:
    """The interactive text-GUI."""

    def __init__(self, console: Console | None = None):
        self.console = console or Console()
        self.agent = PHYSICS_AGENT
        self.compute = ComputeAgent()
        self.running = True
        self.commands: dict[str, Callable[[list[str]], None]] = {
            "solve": self.cmd_solve,
            "explain": self.cmd_explain,
            "simulate": self.cmd_simulate,
            "sims": self.cmd_list_sims,
            "verify": self.cmd_verify,
            "lit": self.cmd_literature,
            "constants": self.cmd_constants,
            "clear": self.cmd_clear,
            "help": self.cmd_help,
            "quit": self.cmd_quit,
            "exit": self.cmd_quit,
        }

    # ---- boot / banner ------------------------------------------------------

    def banner(self) -> Panel:
        return Panel(
            Align.center(Text(BANNER, style="bold cyan")),
            border_style="cyan",
            subtitle="[dim]first-principles physical reasoning  •  virtual laboratory[/dim]",
        )

    # ---- main loop ----------------------------------------------------------

    def loop(self) -> None:
        self.console.print(self.banner())
        self.console.print("[dim]Type 'help' for commands. All simulations render in this UI.[/dim]\n")
        while self.running:
            try:
                line = self.console.input("[bold green]zeno>[/bold green] ").strip()
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[dim]Exiting.[/dim]")
                break
            if not line:
                continue
            try:
                parts = shlex.split(line)
            except ValueError as e:
                self.console.print(f"[red]Parse error:[/red] {e}")
                continue
            cmd, args = parts[0].lower(), parts[1:]
            handler = self.commands.get(cmd)
            if handler is None:
                self.console.print(f"[yellow]Unknown command:[/yellow] {cmd}. Try 'help'.")
                continue
            try:
                handler(args)
            except Exception as e:
                self.console.print(f"[red]Error:[/red] {e}")
                self.console.print(traceback.format_exc(), style="dim red")

    # ---- command handlers ---------------------------------------------------

    def cmd_help(self, args: list[str]) -> None:
        self.console.print(Panel(self.__doc__ or "Zeno help", title="Help", border_style="blue"))

    def cmd_quit(self, args: list[str]) -> None:
        self.running = False
        self.console.print("[dim]Goodbye. Keep questioning.[/dim]")

    def cmd_clear(self, args: list[str]) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def cmd_solve(self, args: list[str]) -> None:
        if not args:
            self.console.print("[yellow]Usage:[/yellow] solve <physics problem>")
            return
        problem = " ".join(args)
        self.console.print(Panel(f"[bold]{problem}[/bold]", title="Problem", border_style="magenta"))
        trace = self.agent.think(problem)
        self.console.print(Panel(trace.as_text(), title="Reasoning trace", border_style="cyan"))
        # safety + verification context
        rep = self.agent.engine.safety.full_check()
        self.console.print(Panel(rep.summary(), title="Physical sanity check", border_style="green"))
        self.console.print(Align.center("[dim]Use 'simulate <name>' to visualise a related system.[/dim]"))

    def cmd_explain(self, args: list[str]) -> None:
        if not args:
            self.console.print("[yellow]Usage:[/yellow] explain <concept>")
            return
        concept = " ".join(args)
        text = self.agent.explain(concept)
        self.console.print(Panel(text, title=f"Explanation: {concept}", border_style="blue"))

    def cmd_list_sims(self, args: list[str]) -> None:
        sims = [m[4:] for m in dir(self.compute) if m.startswith("sim_")]
        table = Table(title="Available simulations", border_style="cyan")
        table.add_column("#", style="dim")
        table.add_column("name", style="bold green")
        for i, s in enumerate(sims, 1):
            table.add_row(str(i), s)
        self.console.print(table)
        self.console.print("[dim]Run with: simulate <name> [key=value ...][/dim]")

    def cmd_simulate(self, args: list[str]) -> None:
        if not args:
            self.cmd_list_sims([])
            return
        name = args[0]
        kwargs = {}
        for tok in args[1:]:
            if "=" in tok:
                k, v = tok.split("=", 1)
                try:
                    val: float | str = float(v)
                except ValueError:
                    val = v
                kwargs[k] = val
        self.console.print(f"[dim]Running simulation '{name}'...[/dim]")
        result = self.compute.run_simulation(name, **kwargs)
        self._render_simulation(result)

    def cmd_verify(self, args: list[str]) -> None:
        if not args:
            self.console.print("[yellow]Usage:[/yellow] verify mass=1.0 speed=3e8 temperature=300")
            return
        values: dict[str, float] = {}
        for tok in args:
            if "=" in tok:
                k, v = tok.split("=", 1)
                try:
                    values[k] = float(v)
                except ValueError:
                    values[k] = v
        rep = self.agent.verify(**values)
        color = "green" if "No unphysical" in rep else "red"
        self.console.print(Panel(rep, title="Physical verification", border_style=color))

    def cmd_literature(self, args: list[str]) -> None:
        if not args:
            self.console.print("[yellow]Usage:[/yellow] lit <query>")
            return
        query = " ".join(args)
        summary = self.agent.literature.summarize(query)
        self.console.print(Panel(summary, title="Literature", border_style="yellow"))

    def cmd_constants(self, args: list[str]) -> None:
        table = Table(title="CODATA Fundamental Constants", border_style="cyan")
        table.add_column("symbol", style="bold")
        table.add_column("name")
        table.add_column("value", justify="right")
        table.add_column("unit")
        for sym, c in CONSTANTS.all().items():
            table.add_row(c.symbol, c.name, f"{c.value:.6g}", c.unit)
        self.console.print(table)

    # ---- simulation rendering (the heart of the UI) -------------------------

    def _render_simulation(self, result) -> None:
        """Render a SimulationResult: metadata table + inline figure + saved PNG."""
        # metadata
        meta_table = Table(title=f"Simulation: {result.name}", border_style="magenta", show_header=False)
        meta_table.add_column("key", style="dim")
        meta_table.add_column("value", style="bold")
        for k, v in result.metadata.items():
            meta_table.add_row(str(k), str(v))
        self.console.print(meta_table)

        # figure
        fig = PLOTTER.new_figure(figsize=(9, 5.5))
        ax = fig.axes[0] if fig.axes else fig.add_subplot(111)
        if result.plotter is not None:
            try:
                result.plotter(result.frames, ax)
            except Exception as e:
                ax.text(0.5, 0.5, f"plot error: {e}", ha="center", color="red")
        else:
            ax.text(0.5, 0.5, f"{result.name} (no plotter)", ha="center", color="#cfd8e3")
        fig.tight_layout()
        png_path = PLOTTER.save(fig, result.name)
        self.console.print(f"[dim]Saved figure:[/dim] [bold blue]{png_path}[/bold blue]")

        # inline render: try rich Image, fall back to ASCII preview
        self._try_inline_image(png_path, result)


    def _try_inline_image(self, png_path: str, result) -> None:
        """Display the rendered figure inline in the terminal when supported."""
        try:
            from rich.image import Image
            img = Image.from_path(png_path)
            self.console.print(Panel(img, title=f"⟨ {result.name} ⟩", border_style="green"))
            return
        except Exception:
            pass
        # Fallback: ASCII preview of 2D data, or a textual note for 1D data
        try:
            self._ascii_preview(result)
        except Exception:
            self.console.print(Panel("[dim](inline image not supported in this terminal; see saved PNG)[/dim]",
                                    border_style="dim"))

    def _ascii_preview(self, result) -> None:
        """Render a small ASCII preview of the simulation data."""
        frames = result.frames
        chars = " .:-=+*#%@"
        if isinstance(frames, np.ndarray) and frames.ndim == 2 and frames.shape[1] >= 2:
            data = frames
            # downsample to ~60 cols x 18 rows
            n_rows, n_cols = 18, min(60, data.shape[0])
            idx = np.linspace(0, data.shape[0] - 1, n_cols).astype(int)
            y = data[idx, 1]
            ymin, ymax = float(np.min(y)), float(np.max(y))
            rng = max(ymax - ymin, 1e-12)
            lines = []
            for row in range(n_rows):
                thr = ymin + (n_rows - 1 - row) * rng / (n_rows - 1)
                line = "".join("█" if yi >= thr else " " for yi in y)
                lines.append(line)
            self.console.print(Panel("\n".join(lines), title=f"ASCII preview: {result.name}",
                                    border_style="green"))
        elif isinstance(frames, dict):
            # measurement counts e.g. bell state
            bars = []
            maxv = max(frames.values()) if frames else 1
            for k, v in frames.items():
                bar_len = int(40 * v / max(maxv, 1))
                bars.append(f"{k:>6} | {'█' * bar_len} {v}")
            self.console.print(Panel("\n".join(bars), title=f"Preview: {result.name}", border_style="green"))
        else:
            self.console.print(Panel(f"[dim]data shape: {getattr(frames, 'shape', '?')}[/dim]",
                                    border_style="dim"))


def run_ui() -> None:
    """Entry point used by main.py."""
    ZenoUI().loop()


if __name__ == "__main__":
    run_ui()
