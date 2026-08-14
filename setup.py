#!/usr/bin/env python3
"""
setup.py - installs dependencies, creates runtime directories, checks perms.

Run:  python setup.py
"""

import os
import subprocess
import sys
from pathlib import Path

REQUIREMENTS = [
    "loguru>=0.7.0",
    "pyyaml>=6.0",
    "requests>=2.31.0",
    "rich>=13.0.0",
    "psutil>=5.9.0",
]
# Optional: enables real Gemini LLM when an API key is configured.
# Without it, the assistant falls back to a deterministic local planner.
OPTIONAL_REQUIREMENTS = [
    "google-generativeai>=0.8.0",
]

RUNTIME_DIRS = ["memory", "logs", "config", "core"]


def install_deps():
    print("[setup] installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", *REQUIREMENTS])


def ensure_dirs(root: Path):
    for d in RUNTIME_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
        print(f"[setup] ensured directory: {d}")


def ensure_secrets(root: Path):
    keys_file = root / "config" / "api_keys.json"
    if not keys_file.exists():
        import json as _json
        template = {
            "GEMINI_API_KEY": "",
            "ANTHROPIC_API_KEY": "",
            "OPENAI_API_KEY": "",
            "GOOGLE_API_KEY": "",
        }
        keys_file.write_text(_json.dumps(template, indent=2) + "\n")
        print("[setup] created config/api_keys.json template")


def main():
    root = Path(__file__).resolve().parent
    ensure_dirs(root)
    ensure_secrets(root)
    try:
        install_deps()
    except subprocess.CalledProcessError as exc:
        print(f"[setup] dependency install failed: {exc}", file=sys.stderr)
    print("[setup] done. Set your API keys in config/api_keys.json then run: python main.py")


if __name__ == "__main__":
    main()
