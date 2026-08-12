"""Pre-configured scaffolding for web, AI, CLI, and mobile apps."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProjectTemplate:
    name: str
    category: str  # web, ai, cli, mobile
    language: str
    files: dict[str, str] = field(default_factory=dict)
    dependencies: list[str] = field(default_factory=list)
    description: str = ""


_TEMPLATES: dict[str, ProjectTemplate] = {
    "python-cli": ProjectTemplate(
        name="python-cli", category="cli", language="python",
        description="A minimal Python CLI with argparse and tests.",
        dependencies=["pytest"],
        files={
            "main.py": '"""CLI entry point."""\nimport argparse\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser(description="My CLI")\n    parser.add_argument("--name", default="world")\n    args = parser.parse_args()\n    print(f"Hello, {args.name}!")\n\n\nif __name__ == "__main__":\n    main()\n',
            "tests/test_main.py": 'from main import main\n\n\ndef test_main(capsys):\n    ...  # add tests\n',
            "requirements.txt": "pytest\n",
            "README.md": "# python-cli\n\nA minimal Python CLI.\n",
        },
    ),
    "fastapi-web": ProjectTemplate(
        name="fastapi-web", category="web", language="python",
        description="A FastAPI REST API with health check.",
        dependencies=["fastapi", "uvicorn", "pytest"],
        files={
            "app/main.py": '"""FastAPI application."""\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n\n@app.get("/health")\ndef health() -> dict[str, str]:\n    return {"status": "ok"}\n',
            "requirements.txt": "fastapi\nuvicorn\n",
            "README.md": "# fastapi-web\n\nRun: `uvicorn app.main:app --reload`\n",
        },
    ),
    "ai-agent": ProjectTemplate(
        name="ai-agent", category="ai", language="python",
        description="A minimal AI agent skeleton with an LLM backbone.",
        dependencies=["google-genai", "rich"],
        files={
            "agent.py": '"""Minimal AI agent skeleton."""\nfrom modeling.neural_backbones import get_backbone\n\n\ndef main(prompt: str) -> str:\n    return get_backbone().fast(prompt).text\n\n\nif __name__ == "__main__":\n    print(main("Hello!"))\n',
            "requirements.txt": "google-genai\nrich\n",
            "README.md": "# ai-agent\n\nSet GEMINI_API_KEY and run `python agent.py`.\n",
        },
    ),
    "react-web": ProjectTemplate(
        name="react-web", category="web", language="typescript",
        description="A React + TypeScript SPA skeleton.",
        dependencies=["react", "react-dom", "vite", "typescript"],
        files={
            "src/App.tsx": "export function App() {\n  return <h1>Hello, React</h1>;\n}\n",
            "index.html": '<!doctype html><html><body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body></html>\n',
            "README.md": "# react-web\n\nUse Vite to run.\n",
        },
    ),
}


class ProjectTemplates:
    """Registry of pre-configured project templates."""

    def __init__(self) -> None:
        self._templates = dict(_TEMPLATES)

    def list(self) -> list[str]:
        return list(self._templates.keys())

    def get(self, name: str) -> ProjectTemplate | None:
        return self._templates.get(name)

    def by_category(self, category: str) -> list[ProjectTemplate]:
        return [t for t in self._templates.values() if t.category == category]

    def register(self, template: ProjectTemplate) -> None:
        self._templates[template.name] = template
