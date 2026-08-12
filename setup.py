"""Installation, environment, and physical-library setup for Zeno.

Run ``python setup.py`` to check that all required Python packages are importable,
that the package tree is intact, and that the simulation registry is populated.
This does NOT modify the system; it only reports status so the user can install
missing dependencies via ``pip install -r requirements.txt``.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


REQUIRED = [
    ("numpy", "numpy"),
    ("scipy", "scipy"),
    ("sympy", "sympy"),
    ("mpmath", "mpmath"),
    ("matplotlib", "matplotlib"),
    ("rich", "rich"),
    ("qutip", "qutip (optional, quantum optics)"),
    ("h5py", "h5py (optional, large datasets)"),
    ("astropy", "astropy (optional, astrophysics constants)"),
    ("numba", "numba (optional, JIT acceleration)"),
]

console = Console()


def check_imports() -> dict[str, bool]:
    results: dict[str, bool] = {}
    for mod, _desc in REQUIRED:
        try:
            importlib.import_module(mod)
            results[mod] = True
        except Exception:
            results[mod] = False
    return results


def check_package_tree(root: Path) -> list[str]:
    """Return list of packages (dirs with __init__.py) found."""
    pkgs = []
    for p in sorted(root.rglob("__init__.py")):
        rel = p.parent.relative_to(root)
        pkgs.append(str(rel))
    return pkgs


def check_simulation_registry() -> list[str]:
    try:
        from agents.compute_agent import ComputeAgent
        ca = ComputeAgent()
        return sorted(m[4:] for m in dir(ca) if m.startswith("sim_"))
    except Exception as e:
        return [f"<error: {e}>"]


def main() -> int:
    root = Path(__file__).resolve().parent
    console.print(Panel("[bold cyan]Zeno — environment & library setup[/bold cyan]", border_style="cyan"))

    # imports
    imp = check_imports()
    t = Table(title="Python dependencies", border_style="blue")
    t.add_column("module"); t.add_column("status")
    for mod, ok in imp.items():
        t.add_row(mod, "[green]OK[/green]" if ok else "[red]MISSING[/red]")
    console.print(t)

    missing = [m for m, ok in imp.items() if not ok and not m.startswith(("qutip", "h5py", "astropy", "numba"))]
    if missing:
        console.print(f"[yellow]Install missing core deps with:[/yellow] pip install -r requirements.txt")

    # package tree
    pkgs = check_package_tree(root)
    console.print(Panel("\n".join(pkgs), title=f"Package tree ({len(pkgs)} packages)", border_style="magenta"))

    # simulations
    sims = check_simulation_registry()
    console.print(Panel("\n".join(sims), title=f"Simulation registry ({len(sims)} sims)", border_style="green"))

    # add root to sys.path so `import zeno` works if run as a package
    if str(root.parent) not in sys.path:
        sys.path.insert(0, str(root.parent))

    console.print("\n[bold green]Setup check complete.[/bold green]")
    console.print("[dim]Launch the assistant with:  python main.py[/dim]")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
