"""Interface with Isabelle/HOL.

Invokes ``isabelle`` when available, otherwise emits theory source.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ISABELLE_AVAILABLE = shutil.which("isabelle") is not None


def is_available() -> bool:
    return ISABELLE_AVAILABLE


def check_theory(theory_name: str, body: str, timeout: int = 120) -> dict[str, Any]:
    if not ISABELLE_AVAILABLE:
        return {"ok": False, "available": False, "output": "isabelle not installed; theory emitted but not checked",
                "theory": body}
    src = f"theory {theory_name}\n  imports Main\nbegin\n{body}\nend\n"
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / f"{theory_name}.thy"
        path.write_text(src)
        try:
            proc = subprocess.run(["isabelle", "process", "-T", theory_name],
                                   input=src, capture_output=True, text=True, timeout=timeout, cwd=td)
            return {"ok": proc.returncode == 0, "available": True, "output": proc.stdout + proc.stderr, "theory": body}
        except subprocess.TimeoutExpired:
            return {"ok": False, "available": True, "output": "timeout", "theory": body}


def emit_theorem(name: str, statement: str, proof: str = "sorry") -> str:
    return f"theorem {name}: \"{statement}\"\n  by {proof}\n"


__all__ = ["is_available", "check_theory", "emit_theorem", "ISABELLE_AVAILABLE"]
