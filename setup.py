"""Installation specs, dependency verifications, and environment setup.

Run ``python setup.py verify`` to check the environment, or
``python setup.py install`` to install the Python dependencies.
"""
from __future__ import annotations

import importlib
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent

REQUIRED_PACKAGES = [
    ("rich", "rich"),
    ("tree_sitter", "tree-sitter"),
    ("ruff", "ruff"),
    ("qdrant_client", "qdrant-client"),
    ("numpy", "numpy"),
    ("requests", "requests"),
    ("watchdog", "watchdog"),
    ("psutil", "psutil"),
]

OPTIONAL_SYSTEM_TOOLS = [
    "git", "python3", "node", "npm", "rustc", "cargo", "go",
    "g++", "java", "sqlite3", "docker",
]


def verify_python() -> bool:
    ok = sys.version_info >= (3, 11)
    print(f"Python {sys.version.split()[0]} ... {'OK' if ok else 'FAIL (need >=3.11)'}")
    return ok


def verify_packages() -> dict[str, bool]:
    results: dict[str, bool] = {}
    for import_name, _ in REQUIRED_PACKAGES:
        try:
            importlib.import_module(import_name)
            results[import_name] = True
            print(f"  package {import_name} ... OK")
        except ImportError:
            results[import_name] = False
            print(f"  package {import_name} ... MISSING")
    return results


def verify_system_tools() -> dict[str, bool]:
    results: dict[str, bool] = {}
    for tool in OPTIONAL_SYSTEM_TOOLS:
        found = shutil.which(tool) is not None
        results[tool] = found
        print(f"  tool {tool} ... {'OK' if found else 'not found'}")
    return results


def verify_structure() -> bool:
    """Verify the expected package directories exist."""
    packages = [
        "agents", "ai_core", "calculations", "capabilities", "config",
        "languages", "lsp_integration", "modeling", "project", "project_engine",
        "repository_workspace", "research", "security_compliance", "simulation",
        "tools", "visualization",
    ]
    # database/ and memory/ are data directories, not Python packages
    data_dirs = ["database", "memory"]
    ok = True
    for pkg in packages:
        init = ROOT / pkg / "__init__.py"
        exists = init.exists()
        print(f"  {pkg}/ ... {'OK' if exists else 'MISSING __init__.py'}")
        if not exists:
            ok = False
    for d in data_dirs:
        exists = (ROOT / d).is_dir()
        print(f"  {d}/ (data) ... {'OK' if exists else 'MISSING'}")
        if not exists:
            ok = False
    return ok


def install() -> int:
    """Install Python dependencies from requirements.txt."""
    req = ROOT / "requirements.txt"
    if not req.exists():
        print("requirements.txt not found.")
        return 1
    print("Installing dependencies...")
    return subprocess.call([sys.executable, "-m", "pip", "install", "-r", str(req)])


def verify() -> int:
    """Run full environment verification."""
    print("=== CODING_AI Environment Verification ===\n")
    ok = verify_python()
    print("\nPython packages:")
    pkg_ok = all(verify_packages().values())
    print("\nSystem tools (optional):")
    verify_system_tools()
    print("\nProject structure:")
    struct_ok = verify_structure()
    print("\n=== Summary ===")
    print(f"Python:      {'OK' if ok else 'FAIL'}")
    print(f"Packages:    {'OK' if pkg_ok else 'MISSING (run: python setup.py install)'}")
    print(f"Structure:   {'OK' if struct_ok else 'INCOMPLETE'}")
    if ok and struct_ok:
        print("\nCore environment ready. Optional packages/tools enhance capabilities.")
        return 0
    return 1


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv or argv[0] in ("verify", "check"):
        return verify()
    if argv[0] == "install":
        return install()
    print(f"Usage: python setup.py [verify|install]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
