"""Main entry point for the Biology AI application.

Usage:
    python main.py            # launch the desktop GUI (default)
    python main.py --cli      # interactive text REPL
    python main.py --status   # print system status and exit
    python main.py --query "your biology question"
"""
from __future__ import annotations

import argparse
import json
import sys


BANNER = r"""
 ____  _ ___   ___      _   _      _ _    _       ___  ____ ___  ____
| __ )| / _ \ / _ \    | | | |_ __(_) |__| | ___ / _ \/ ___/ _ \|  _ \
|  _ \| | | | | | | |__| |_| | '__| | '_ \ |/ _ \ | | | |  | | | | |_) |
| |_) | | |_| | |_| |____|\  _/| |  | | |_) | (_) | |_| | |__| |_| |  __/
|____/|_|\___/ \___/      |_|  |_|  |_|_.__/ \___/ \___/ \____\___/|_|

  Autonomous Biology Laboratory Assistant  (Gemini 2.5/1.5 Flash engines)
"""


def print_banner():
    print(BANNER)


def cli_mode():
    print_banner()
    from agents.biology_agent import BiologyAgent
    agent = BiologyAgent()
    print(f"Agents loaded. AI engine status: {agent.ai.status()}\n")
    print("Type your biology question, 'status' for system info, or 'exit' to quit.\n")
    while True:
        try:
            q = input("biology-ai> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if not q:
            continue
        if q.lower() in ("exit", "quit"):
            print("Goodbye.")
            break
        if q.lower() == "status":
            print(json.dumps(agent.status(), indent=2, default=str))
            continue
        try:
            print("\n" + str(agent.route(q)) + "\n" + "-" * 60 + "\n")
        except Exception as e:
            print(f"[ERROR] {e}\n")


def gui_mode():
    try:
        import ui
    except Exception as e:
        print(f"GUI launch failed ({e}); falling back to CLI mode.")
        cli_mode()
        return
    ui.launch()


def status_mode():
    from ai_core.ai_engine import AIEngine
    print(json.dumps(AIEngine().status(), indent=2, default=str))


def query_mode(query: str):
    from agents.biology_agent import BiologyAgent
    agent = BiologyAgent()
    print(str(agent.route(query)))


def main():
    parser = argparse.ArgumentParser(description="Biology AI - Autonomous Laboratory Assistant")
    parser.add_argument("--cli", action="store_true", help="Run in interactive text mode")
    parser.add_argument("--gui", action="store_true", help="Launch the tkinter GUI (default)")
    parser.add_argument("--status", action="store_true", help="Print system status and exit")
    parser.add_argument("--query", type=str, help="Run a single query and exit")
    args = parser.parse_args()

    if args.status:
        status_mode()
        return
    if args.query:
        query_mode(args.query)
        return
    if args.cli:
        cli_mode()
        return
    gui_mode()


if __name__ == "__main__":
    main()
