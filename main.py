"""CODING_AI application entry point.

Wires the AI engine, UI, and project management together and starts the
interactive REPL. Can also be used programmatically.
"""
from __future__ import annotations

import argparse
import sys
from typing import Any

from ai_core.ai_engine import AIEngine
from ui import UI


def build_engine(workspace: str = ".") -> AIEngine:
    """Construct the AI engine with default configuration."""
    return AIEngine(workspace=workspace)


def run_repl(workspace: str = ".") -> None:
    """Start the interactive text UI."""
    engine = build_engine(workspace)
    ui = UI(engine=engine)
    ui.run()


def run_once(prompt: str, workspace: str = ".") -> None:
    """Execute a single natural-language request and print the result."""
    engine = build_engine(workspace)
    result = engine.handle(prompt)
    if result.success:
        print(result.content)
    else:
        print(f"Error: {result.error}", file=sys.stderr)
        sys.exit(1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="zeno",
        description="CODING_AI — a capability-based coding AI powered by Gemini.",
    )
    parser.add_argument("prompt", nargs="?", default=None,
                        help="A natural-language request. If omitted, starts the REPL.")
    parser.add_argument("-w", "--workspace", default=".",
                        help="Workspace directory (default: current directory).")
    parser.add_argument("--version", action="version", version="CODING_AI 1.0.0")
    args = parser.parse_args(argv)

    if args.prompt:
        run_once(args.prompt, args.workspace)
    else:
        run_repl(args.workspace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
