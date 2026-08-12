"""Text-GUI user interface for the Mathematics AI.

A simple REPL that dispatches queries to the :class:`MathAgent`. All
simulations and interactions are driven from this interface, as required by
the spec ("ALL SIMULATIONS ARE DONE ON THE USER INTERFACE").
"""

from __future__ import annotations

import re
import shlex
import sys
from typing import Any

import sympy as sp

from mathematics_ai.agents.base import AgentResult
from mathematics_ai.agents.math_agent import MathAgent


def sympy_lambda(expr: str):
    """Parse a string expression into a single-variable numeric function."""
    parsed = sp.sympify(expr)
    free = list(parsed.free_symbols)
    var = free[0] if free else sp.Symbol("x")
    return sp.lambdify(var, parsed, "numpy")


HELP_TEXT = """\
Mathematics AI — commands
  <query>            Solve / prove / explore a math problem
  help               Show this help
  domain <text>      Classify the mathematical domain of <text>
  prove <stmt>        Attempt a formal proof of <stmt>
  compute <expr>      Evaluate a computation query
  sequence <nums>    Detect patterns in a sequence (space- or comma-separated)
  optimize <expr>    Minimize a function
  oeis <nums>        Look up integer sequences in OEIS
  project create <name>: <goal>   Start a research project
  project list       List research projects
  paper <title>      Generate an AMS-style LaTeX skeleton
  clear              Clear screen
  quit | exit        Leave
"""


class MathematicsUI:
    """REPL interface wrapping :class:`MathAgent`."""

    BANNER = r"""
  __  __      _    _   _      _   ___      _           ___        _   ___  ___  ___
 |  \/  | ___| |__| \ | | ___| |_( _ ) ___| |__  ___  | _ ) __ _ / | / __|| _ \/ __|
 | |\/| |/ _ \ '_ \  \| |/ _ \ __/ _ \/ _ \ '_ \/ -_) | _ \/ _` | | \__ \|  _/ (_-<
 |_|  |_|\___/_|_/_|\__|\___/\__\___/\___/_.__/\___| |___/\__,_|_| |___/|_|  \__/

  Autonomous AI Mathematics Assistant & Research Environment
  Type 'help' for commands. 'quit' to exit.
"""

    def __init__(self, agent: MathAgent | None = None) -> None:
        self.agent = agent or MathAgent()
        self._commands = {
            "help": self._cmd_help,
            "domain": self._cmd_domain,
            "prove": self._cmd_prove,
            "compute": self._cmd_compute,
            "sequence": self._cmd_sequence,
            "optimize": self._cmd_optimize,
            "oeis": self._cmd_oeis,
            "project": self._cmd_project,
            "paper": self._cmd_paper,
            "clear": self._cmd_clear,
            "quit": self._cmd_quit,
            "exit": self._cmd_quit,
        }
        self._running = True

    # ------------------------------------------------------------------ run loop
    def run(self) -> None:
        print(self.BANNER)
        engine_status = "Gemini" if self._gemini_available() else "local fallback"
        print(f"  [engine: {engine_status}]\n")
        while self._running:
            try:
                line = input("math> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not line:
                continue
            self.dispatch(line)

    def dispatch(self, line: str) -> None:
        parts = shlex.split(line)
        cmd = parts[0].lower()
        handler = self._commands.get(cmd)
        if handler is not None:
            handler(parts[1:])
        else:
            # default: treat the whole line as a natural-language query
            result = self.agent.solve(line)
            self._print_result(result)

    # ------------------------------------------------------------------ commands
    def _cmd_help(self, _args: list[str]) -> None:
        print(HELP_TEXT)

    def _cmd_domain(self, args: list[str]) -> None:
        text = " ".join(args)
        result = self.agent.planning.detect_domain(text)
        print(f"Domain: {result}")

    def _cmd_prove(self, args: list[str]) -> None:
        stmt = " ".join(args)
        result = self.agent.solve(f"prove that {stmt}")
        self._print_result(result)

    def _cmd_compute(self, args: list[str]) -> None:
        result = self.agent.solve(" ".join(args))
        self._print_result(result)

    def _cmd_sequence(self, args: list[str]) -> None:
        nums = _parse_ints(" ".join(args))
        result = self.agent.conjecture.generate_from_sequence(nums, name="ui_query")
        self._print_result(result)

    def _cmd_optimize(self, args: list[str]) -> None:
        expr = " ".join(args)
        m = re.search(r"on\s*\[(-?\d+\.?\d*),\s*(-?\d+\.?\d*)\]", expr)
        if m:
            a, b = float(m.group(1)), float(m.group(2))
            body = re.sub(r"\s+on\s*\[.*\]", "", expr).strip()
            try:
                f = sympy_lambda(body)
                result = self.agent.optimization.constrained(f, [(a, b)], [(a + b) / 2])
            except Exception as e:
                print(f"  error parsing expression: {e}")
                return
        else:
            try:
                f = sympy_lambda(expr)
            except Exception as e:
                print(f"  error parsing expression: {e}")
                return
            result = self.agent.optimization.minimize(f, [1.0])
        self._print_result(result)

    def _cmd_oeis(self, args: list[str]) -> None:
        nums = _parse_ints(" ".join(args))
        result = self.agent.research.search_sequence(nums)
        self._print_result(result)

    def _cmd_project(self, args: list[str]) -> None:
        if not args:
            print("usage: project create <name>: <goal> | project list")
            return
        sub = args[0]
        if sub == "list":
            result = self.agent.project.list_projects()
            for p in (result.answer or []):
                print(f"  [{p['id']}] {p.get('title')} ({p.get('status')})")
        elif sub == "create":
            rest = " ".join(args[1:])
            if ":" not in rest:
                print("usage: project create <name>: <goal>")
                return
            name, goal = rest.split(":", 1)
            result = self.agent.project.create_project(name.strip(), goal.strip())
            self._print_result(result)
        else:
            print(f"unknown project subcommand: {sub}")

    def _cmd_paper(self, args: list[str]) -> None:
        title = " ".join(args) or "Untitled"
        from mathematics_ai.project.paper_generator import generate_paper
        tex = generate_paper(
            title=title,
            authors=["Mathematics AI"],
            abstract="Auto-generated skeleton. Replace with your abstract.",
            sections=[{"heading": "Introduction", "content": "TODO"}],
        )
        print(tex)

    def _cmd_clear(self, _args: list[str]) -> None:
        print("\033[2J\033[H", end="")

    def _cmd_quit(self, _args: list[str]) -> None:
        self._running = False

    # ------------------------------------------------------------------ helpers
    def _print_result(self, result: Any) -> None:
        if isinstance(result, AgentResult):
            if result.success:
                print(f"  ✓ answer: {result.answer}")
                for s in result.steps:
                    print(f"    step: {s}")
                if result.metadata:
                    print(f"    meta: {result.metadata}")
            else:
                print(f"  ✗ failed: {result.error or 'unknown error'}")
        elif isinstance(result, dict):
            for k, v in result.items():
                print(f"  {k}: {v}")
        else:
            print(result)

    def _gemini_available(self) -> bool:
        try:
            return bool(self.agent.advanced and self.agent.advanced.available)
        except Exception:
            return False


def _parse_ints(text: str) -> list[int]:
    cleaned = text.replace(",", " ")
    return [int(x) for x in cleaned.split() if x.lstrip("-").isdigit()]


def main() -> None:
    MathematicsUI().run()


if __name__ == "__main__":
    main()
