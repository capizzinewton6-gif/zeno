"""Interface with the Coq proof assistant.

Mirrors the Lean interface: invokes ``coqc`` when available, otherwise emits
Coq source and reports unavailability.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

COQ_AVAILABLE = shutil.which("coqc") is not None


def is_available() -> bool:
    return COQ_AVAILABLE


def check_declaration(declaration: str, timeout: int = 60) -> dict[str, Any]:
    if not COQ_AVAILABLE:
        return {"ok": False, "available": False, "output": "coqc not installed; declaration emitted but not checked",
                "declaration": declaration}
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "check.v"
        path.write_text(declaration + "\n")
        try:
            proc = subprocess.run(["coqc", str(path)], capture_output=True, text=True, timeout=timeout, cwd=td)
            return {"ok": proc.returncode == 0, "available": True, "output": proc.stdout + proc.stderr, "declaration": declaration}
        except subprocess.TimeoutExpired:
            return {"ok": False, "available": True, "output": "timeout", "declaration": declaration}


def emit_theorem(name: str, statement: str, proof: str = "admit.") -> str:
    return f"Theorem {name} : {statement}.\nProof.\n  {proof}\nQed.\n"


__all__ = ["is_available", "check_declaration", "emit_theorem", "COQ_AVAILABLE"]
