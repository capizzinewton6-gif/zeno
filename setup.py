"""
VISION_AI - Autonomous AI Vision & Scene Understanding Assistant.

This is a text-GUI-based AI Vision assistant. Visual intelligence is provided
exclusively by Google Gemini (2.5 Flash + 1.5 Flash); local OpenCV code handles
camera capture, preprocessing, geometry, NMS, calibration, and visualization.
"""

from setuptools import setup, find_packages

setup(
    name="vision_ai",
    version="0.1.0",
    description="Autonomous AI Vision & Scene Understanding Assistant (Gemini-powered)",
    author="OpenHands",
    python_requires=">=3.9",
    packages=find_packages(include=[
        "agents", "agents.*",
        "core_vision", "core_vision.*",
        "facial_processing", "facial_processing.*",
        "tracking_analytics", "tracking_analytics.*",
        "modeling", "modeling.*",
        "calculations", "calculations.*",
        "simulation", "simulation.*",
        "edge_computing", "edge_computing.*",
        "visualization", "visualization.*",
        "vision_input", "vision_input.*",
        "security_compliance", "security_compliance.*",
        "research", "research.*",
        "project", "project.*",
        "tools", "tools.*",
        "ai_core", "ai_core.*",
        "src.gemini_25_flash_engine", "src.gemini_25_flash_engine.*",
        "src.gemini_15_flash_engine", "src.gemini_15_flash_engine.*",
    ]),
    install_requires=[
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "Pillow>=10.0.0",
        "requests>=2.31.0",
        "google-genai>=0.7.0",
        "google-generativeai>=0.7.0",
    ],
    entry_points={"console_scripts": ["vision-ai=main:main"]},
)
