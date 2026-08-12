"""Installation and configuration for the Biology AI application.

This setup.py allows `pip install -e .` for development and provides a small
helper for first-time configuration checks.

Run directly to validate the environment:
    python setup.py check
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from setuptools import find_packages, setup

HERE = Path(__file__).parent


def _read_requirements():
    req_path = HERE / "requirements.txt"
    if req_path.exists():
        return [line.strip() for line in req_path.read_text().splitlines()
                if line.strip() and not line.startswith("#")]
    return []


setup(
    name="biology-ai",
    version="0.1.0",
    description="Autonomous Biology Laboratory Assistant powered by Gemini Flash",
    author="Biology AI",
    python_requires=">=3.10",
    packages=find_packages(include=[
        "agents", "agents.*",
        "biology", "biology.*",
        "genetic_engineering", "genetic_engineering.*",
        "modeling", "modeling.*",
        "calculations", "calculations.*",
        "simulation", "simulation.*",
        "genomics_bioinformatics", "genomics_bioinformatics.*",
        "lab_automation", "lab_automation.*",
        "prototyping", "prototyping.*",
        "biomaterials", "biomaterials.*",
        "vision", "vision.*",
        "biosafety_hazards", "biosafety_hazards.*",
        "research", "research.*",
        "project", "project.*",
        "tools", "tools.*",
        "ai_core", "ai_core.*",
        "src", "src.*",
        "config", "config.*",
        "memory", "memory.*",
    ]),
    install_requires=_read_requirements(),
    entry_points={"console_scripts": ["biology-ai=main:main"]},
)


def check_environment() -> dict:
    """Report on installed dependencies and AI engine availability."""
    report = {"python": sys.version.split()[0], "platform": sys.platform}
    optional = ["numpy", "scipy", "matplotlib", "Bio",
                "rich", "google.generativeai", "google.genai"]
    for mod in optional:
        try:
            __import__(mod)
            report[mod] = "ok"
        except Exception as e:
            report[mod] = f"missing ({e})"
    try:
        from ai_core.ai_engine import AIEngine
        report["ai_engine"] = AIEngine().status()
    except Exception as e:
        report["ai_engine"] = f"error ({e})"
    return report


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        import json
        print(json.dumps(check_environment(), indent=2, default=str))
    else:
        # Run setup() when invoked as `python setup.py ...` or via pip
        setup()  # type: ignore[call-arg]
