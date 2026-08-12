"""Interface with the Lean 4 theorem prover.

When ``elan``/``lean`` is on PATH, this module can invoke Lean to check
declarations. Otherwise it emits Lean 4 source and returns a clear "not
installed" status so callers can degrade gracefully.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

LEAN_AVAILABLE = shutil.which("lean") is not None


def is_available() -> bool:
    return LEAN_AVAILABLE


def check_declaration(declaration: str, timeout: int = 60) -> dict[str, Any]:
    """Write a Lean file and attempt to check it.

    Returns {"ok": bool, "output": str, "available": LEAN_AVAILABLE}.
    """
    if not LEAN_AVAILABLE:
        return {"ok": False, "available": False, "output": "lean not installed; declaration emitted but not checked",
                "declaration": declaration}
    src = "import Mathlib\n\n" + declaration + "\n"
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "Check.lean"
        path.write_text(src)
        try:
            proc = subprocess.run(["lean", str(path)], capture_output=True, text=True, timeout=timeout)
            return {"ok": proc.returncode == 0, "available": True, "output": proc.stdout + proc.stderr, "declaration": declaration}
        except subprocess.TimeoutExpired:
            return {"ok": False, "available": True, "output": "timeout", "declaration": declaration}


def emit_theorem(name: str, statement: str, proof: str = "sorry") -> str:
    """Emit a Lean 4 theorem declaration."""
    return f"theorem {name} : {statement} := by\n  {proof}\n"


__all__ = ["is_available", "check_declaration", "emit_theorem", "LEAN_AVAILABLE"]
