"""Installation setup for the Screen Recognition AI."""

from setuptools import setup, find_packages
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LONG_DESC = (ROOT / "ai_core" / "prompt.txt").read_text(encoding="utf-8") if (ROOT / "ai_core" / "prompt.txt").exists() else "Screen Recognition AI"

setup(
    name="screen-recognition-ai",
    version="1.0.0",
    description="A Gemini-powered screen recognition and automation AI",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    author="Screen AI",
    license="MIT",
    python_requires=">=3.9",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=[
        # Core dependencies are listed in requirements.txt; this mirrors them.
    ],
    extras_require={
        "full": [
            "google-generativeai>=0.7.0",
            "google-genai>=0.3.0",
            "opencv-python>=4.9.0",
            "Pillow>=10.2.0",
            "numpy>=1.26.0",
            "pytesseract>=0.3.10",
            "mss>=9.0.0",
            "pyautogui>=0.9.54",
            "pyperclip>=1.8.2",
            "psutil>=5.9.0",
            "cryptography>=42.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "screen-ai=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
