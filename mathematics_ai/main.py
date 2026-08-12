"""Main entry point for the Mathematics AI.

Usage:
    python -m mathematics_ai.main            # interactive REPL
    python -m mathematics_ai.main "query"     # one-shot query
    python -m mathematics_ai.main --batch file.txt  # run queries from a file
"""

from __future__ import annotations

import sys
from pathlib import Path

from mathematics_ai.agents.math_agent import MathAgent
from mathematics_ai.ui import MathematicsUI, _parse_ints


def one_shot(query: str, agent: MathAgent | None = None) -> None:
    """Solve a single query and print the result."""
    agent = agent or MathAgent()
    result = agent.solve(query)
    print(f"Query: {query}")
    if result.success:
        print(f"Answer: {result.answer}")
    else:
        print(f"Failed: {result.error}")
    if result.steps:
        print("Steps:")
        for s in result.steps:
            print(f"  - {s}")
    if result.metadata:
        print(f"Meta: {result.metadata}")


def batch(path: str, agent: MathAgent | None = None) -> None:
    """Run each non-empty, non-comment line of a file as a query."""
    agent = agent or MathAgent()
    lines = Path(path).read_text().splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        print("=" * 60)
        one_shot(line, agent)


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    if not argv:
        MathematicsUI().run()
        return 0
    if argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--batch" and len(argv) > 1:
        batch(argv[1])
        return 0
    query = " ".join(argv)
    one_shot(query)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
