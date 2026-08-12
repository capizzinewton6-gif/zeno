#!/usr/bin/env python3
"""
setup.py - installs dependencies, creates runtime directories and config.

Run:  python setup.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REQUIREMENTS = [
    "rich>=13.0.0",
    "psutil>=5.9.0",
    "numpy>=1.24.0",
    "requests>=2.31.0",
    "google-generativeai>=0.8.0",
    "pyyaml>=6.0",
]

RUNTIME_DIRS = ["logs", "scenes", "memory"]


def install_deps():
    print("[setup] installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", *REQUIREMENTS])


def ensure_dirs():
    for d in RUNTIME_DIRS:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
        print(f"[setup] ensured directory: {d}")


def ensure_config():
    cfg = ROOT / "config"
    cfg.mkdir(parents=True, exist_ok=True)
    defaults = {
        "settings.json": {
            "user": "Operator",
            "boot_sequence": True,
            "spatial_audio": True,
            "particle_effects": True,
        },
        "hardware.json": {
            "depth_camera": {"type": "auto", "enabled": True},
            "projector": {"type": "auto", "brightness": 1.0},
            "safety_interlock": True,
        },
        "display.json": {
            "resolution": [3840, 2160],
            "parallax": "full",
            "lightfield": True,
            "target_fps": 60,
        },
        "ai_keys.json": {"gemini_api_key": "", "model_25": "gemini-2.5-flash", "model_15": "gemini-1.5-flash"},
    }
    for name, data in defaults.items():
        path = cfg / name
        if not path.exists():
            path.write_text(json.dumps(data, indent=2))
            print(f"[setup] wrote default config: {name}")
        else:
            print(f"[setup] config exists: {name}")


def main():
    ensure_dirs()
    ensure_config()
    if "--no-deps" not in sys.argv:
        install_deps()
    print("[setup] complete. Run:  python main.py")


if __name__ == "__main__":
    main()
