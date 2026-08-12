"""setup module — Installation and configuration for Chemistry AI."""

import os
import json
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def install_requirements():
    """Install Python dependencies from requirements.txt."""
    req_path = os.path.join(HERE, "requirements.txt")
    if not os.path.exists(req_path):
        return {"status": "error", "message": "requirements.txt not found"}
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
        return {"status": "ok", "message": "Dependencies installed."}
    except subprocess.CalledProcessError as exc:
        return {"status": "error", "message": str(exc)}


def init_databases():
    from database import init_all
    return init_all()


def load_config(name="settings.json"):
    path = os.path.join(HERE, "config", name)
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def setup_check():
    """Verify the installation is complete."""
    checks = {
        "python": sys.version.split()[0],
        "requirements_file": os.path.exists(os.path.join(HERE, "requirements.txt")),
        "config_dir": os.path.exists(os.path.join(HERE, "config")),
        "memory_dir": os.path.exists(os.path.join(HERE, "memory")),
        "ai_core": os.path.exists(os.path.join(HERE, "ai_core", "ai_engine.py")),
        "agents": os.path.exists(os.path.join(HERE, "agents", "chemistry_agent.py")),
        "main_app": os.path.exists(os.path.join(HERE, "main.py")),
    }
    # Optional packages
    optional = {}
    for pkg in ["flask", "numpy", "scipy", "matplotlib", "pandas", "rdkit", "google.generativeai"]:
        try:
            __import__(pkg.split(".")[0])
            optional[pkg] = True
        except Exception:
            optional[pkg] = False
    checks["optional_packages"] = optional
    return checks


def full_setup():
    """Run complete setup: install deps, init databases."""
    results = {}
    results["install"] = install_requirements()
    results["databases"] = init_databases()
    results["check"] = setup_check()
    return results


if __name__ == "__main__":
    print(json.dumps(full_setup(), indent=2, default=str))
