#!/usr/bin/env python3
"""
TONY STARK HOLOGRAM OS - main entry point.

Boots the arc reactor, spatially scans the room, raises the holographic grid,
materialises the telemetry dashboard, greets the user, then exposes the
interactive holographic workspace.

Usage:
    python main.py                  # full boot + interactive workspace
    python main.py --task "..."     # single command
    python main.py --skip-boot      # skip the boot animation
    python main.py --no-daemons     # skip background daemons
"""

from __future__ import annotations

import argparse
import sys
import threading
import time
from typing import Optional

from core.arc_reactor import ArcReactor
from core.hologram_grid import HologramGrid
from core.startup import StartupSequence
from core.telemetry_dashboard import TelemetryDashboard
from core.workspace import HolographicWorkspace
from ui import HolographicUI


def parse_args():
    p = argparse.ArgumentParser(description="Tony Stark Hologram OS")
    p.add_argument("--task", "-t", type=str, default=None, help="Single command to execute")
    p.add_argument("--skip-boot", action="store_true", help="Skip the boot sequence")
    p.add_argument("--no-daemons", action="store_true", help="Skip background daemons")
    p.add_argument("--user", type=str, default="Operator", help="User display name")
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    return p.parse_args()


def boot_sequence(user: str, ui: "HolographicUI"):
    """Run the cinematic startup experience."""
    reactor = ArcReactor(ui=ui)
    grid = HologramGrid(ui=ui)
    dashboard = TelemetryDashboard(ui=ui)
    boot = StartupSequence(reactor=reactor, grid=grid, dashboard=dashboard, ui=ui)
    boot.run(user=user)


def start_daemons(workspace: HolographicWorkspace):
    """Background telemetry / safety / ai-bridge loops."""
    threads = []

    def loop(fn, name, interval):
        while True:
            try:
                fn()
            except Exception as exc:
                print(f"[daemon:{name}] error: {exc}", file=sys.stderr)
            time.sleep(interval)

    specs = [
        (workspace.dashboard.refresh, "telemetry", 5),
        (workspace.tick_safety, "safety", 2),
    ]
    for fn, name, interval in specs:
        t = threading.Thread(target=loop, args=(fn, name, interval), daemon=True, name=f"daemon-{name}")
        t.start()
        threads.append(t)
    print("[main] background daemons started:", [t.name for t in threads])
    return threads


def main():
    args = parse_args()
    ui = HolographicUI(verbose=args.verbose)

    if not args.skip_boot:
        boot_sequence(args.user, ui)
    else:
        print("[boot] skipped")

    workspace = HolographicWorkspace(ui=ui)

    if not args.no_daemons:
        start_daemons(workspace)

    if args.task:
        result = workspace.execute(args.task)
        ui.speak(result)
        return

    ui.run_workspace(workspace)


if __name__ == "__main__":
    main()
