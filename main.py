"""Main entry point for the Zeno AI Inventor.

Usage:
    python main.py              # interactive text UI
    python main.py invent "..." # one-shot invention workflow
    python main.py engineer "..." # one-shot engineering solve
"""

from __future__ import annotations

import sys

from ai_core.ai_engine import AIEngine
from ui import ZenoUI


def main(argv: list[str] | None = None):
    argv = argv if argv is not None else sys.argv[1:]
    engine = AIEngine()

    if not argv:
        ZenoUI(engine).loop()
        return 0

    cmd = argv[0].lower()
    arg = " ".join(argv[1:])

    if cmd in ("-h", "--help", "help"):
        print(__doc__)
        return 0

    ui = ZenoUI(engine)
    if cmd == "invent" and arg:
        ui._run_invention(arg)
    elif cmd == "engineer" and arg:
        print(ui.engineering.solve(arg))
    elif cmd == "design" and arg:
        print(ui.design.design(arg))
    elif cmd == "research" and arg:
        print(ui.research.research(arg))
    elif cmd == "models":
        ui.show_models()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
