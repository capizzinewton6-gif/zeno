#!/usr/bin/env python3
"""
Autonomous Computer AI Assistant - main entry point.

Starts the smart orchestrator, all background daemons (sensors, autonomy,
security) and launches the text-based UI.

Usage:
    python main.py                     # interactive mode
    python main.py --task "..."        # single task mode
    python main.py --no-daemons        # skip background daemons
"""

import argparse
import sys
import threading
import time

from smart_orchestrator import SmartOrchestrator
from ui import TextUI


def parse_args():
    p = argparse.ArgumentParser(description="Autonomous Computer AI Assistant")
    p.add_argument("--task", "-t", type=str, default=None, help="Single task to execute")
    p.add_argument("--no-daemons", action="store_true", help="Skip background daemons")
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    return p.parse_args()


def start_daemons(orchestrator: SmartOrchestrator):
    """Spin up sensor / autonomy / security background loops."""
    daemons = []

    def loop(fn, name, interval):
        while True:
            try:
                fn()
            except Exception as exc:
                print(f"[daemon:{name}] error: {exc}", file=sys.stderr)
            time.sleep(interval)

    specs = [
        (getattr(orchestrator.sensors, "poll_all", lambda: None), "sensors", 30),
        (getattr(orchestrator.autonomy, "tick", lambda: None), "autonomy", 15),
        (getattr(orchestrator.security, "audit_tick", lambda: None), "security", 60),
    ]
    for fn, name, interval in specs:
        t = threading.Thread(target=loop, args=(fn, name, interval), daemon=True, name=f"daemon-{name}")
        t.start()
        daemons.append(t)
    print("[main] background daemons started:", [d.name for d in daemons])
    return daemons


def main():
    args = parse_args()
    orchestrator = SmartOrchestrator()

    if not args.no_daemons:
        start_daemons(orchestrator)

    if args.task:
        result = orchestrator.run(args.task)
        print(f"\nAssistant: {result}\n")
        return

    ui = TextUI(orchestrator)
    ui.run()


if __name__ == "__main__":
    main()
