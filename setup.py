from setuptools import setup, find_packages

setup(
    name="zeno-ai-inventor",
    version="1.0.0",
    description="Autonomous AI Inventor, Engineer & Research Assistant",
    author="Zeno",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "google-generativeai>=0.7.0",
        "google-genai>=0.3.0",
        "requests>=2.31.0",
        "Pillow>=10.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
    ],
    entry_points={
        "console_scripts": [
            "zeno=main:main",
        ],
    },
)
