#!/usr/bin/env python3
"""Text-based UI for the Autonomous Computer AI Assistant."""

import sys

try:
    from rich.console import Console
    from rich.panel import Panel

    _CONSOLE = Console()
    _HAS_RICH = True
except ImportError:
    _CONSOLE = None
    _HAS_RICH = False


def _print(text: str):
    if _HAS_RICH:
        _CONSOLE.print(Panel.fit(text, title="Assistant"))
    else:
        print(f"\nAssistant: {text}\n")


class TextUI:
    """Simple REPL that drives the smart orchestrator."""

    BANNER = (
        "=" * 60
        + "\n  Autonomous Computer AI Assistant\n"
        + "  Gemini 2.5 Flash (reasoning) + Gemini 1.5 Flash (processing)\n"
        + "  Type 'exit' to quit\n"
        + "=" * 60
    )

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def run(self):
        print(self.BANNER)
        while True:
            try:
                user_input = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nShutting down.")
                break
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit", "bye"}:
                print("Shutting down.")
                break
            try:
                result = self.orchestrator.run(user_input)
            except Exception as exc:
                result = f"I hit an error: {exc}"
            _print(result)


if __name__ == "__main__":
    from smart_orchestrator import SmartOrchestrator

    TextUI(SmartOrchestrator()).run()
