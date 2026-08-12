#!/usr/bin/env python3
"""Zeno — Autonomous AI Physics Assistant & Virtual Laboratory.

Main entry point. Run interactively:

    python main.py

or non-interactively to execute a single command and exit:

    python main.py --cmd "simulate harmonic_oscillator"
    python main.py --cmd "solve 'derive the period of a simple pendulum'"
    python main.py --cmd "constants"
    python main.py --setup            # run environment check only
"""

from __future__ import annotations

import argparse
import sys

from rich.console import Console

from ui import ZenoUI


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="zeno",
        description="Zeno — Autonomous AI Physics Assistant & Virtual Laboratory",
    )
    parser.add_argument("--cmd", type=str, default=None,
                        help="Run a single command non-interactively and exit.")
    parser.add_argument("--setup", action="store_true",
                        help="Run the environment/library check and exit.")
    args = parser.parse_args(argv)

    if args.setup:
        import runpy
        runpy.run_path("setup.py", run_name="__main__")
        return 0

    console = Console()
    ui = ZenoUI(console=console)

    if args.cmd:
        # non-interactive single command
        console.print(ui.banner())
        line = args.cmd
        import shlex
        parts = shlex.split(line)
        cmd, rest = parts[0].lower(), parts[1:]
        handler = ui.commands.get(cmd)
        if handler is None:
            console.print(f"[red]Unknown command:[/red] {cmd}")
            return 1
        try:
            handler(rest)
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            import traceback
            console.print(traceback.format_exc(), style="dim red")
            return 1
        return 0

    ui.loop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
