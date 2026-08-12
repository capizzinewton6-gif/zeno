"""Installation and configuration for the Mathematics AI.

Run `python setup.py install` or, preferably, `pip install -e .` to install
the package in development mode. The package itself is dependency-light at
import time; heavy scientific dependencies are imported lazily by each
capability module so that the CLI starts quickly.
"""

from setuptools import setup, find_packages
from pathlib import Path

ROOT = Path(__file__).parent
long_description = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else "Autonomous AI Mathematics Assistant"

setup(
    name="mathematics_ai",
    version="0.1.0",
    description="Autonomous AI Mathematics Assistant and research environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mathematics AI",
    license="MIT",
    packages=find_packages(include=["mathematics_ai", "mathematics_ai.*"]),
    python_requires=">=3.10",
    install_requires=[
        "sympy>=1.12",
        "numpy>=1.26",
        "scipy>=1.11",
        "mpmath>=1.3",
        "networkx>=3.2",
        "matplotlib>=3.8",
        "google-genai>=0.3.0",
    ],
    entry_points={
        "console_scripts": [
            "math-ai=mathematics_ai.main:main",
        ],
    },
)
