"""Best-practice coding standards and linting rule sets.

Provides language-agnostic rule sets plus helpers to materialize linter configs
(ruff, eslint, etc.) so agents apply consistent standards across edits.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# Language-agnostic core principles -----------------------------------------
PRINCIPLES: tuple[str, ...] = (
    "Single Responsibility per module.",
    "Minimal, focused diffs over rewrites.",
    "Explicit is better than implicit.",
    "Fail fast with precise errors.",
    "No premature optimization; measure first.",
    "Tests cover behavior, not implementation.",
    "Security by default; validate at every boundary.",
    "Comments only for the non-obvious.",
)


@dataclass
class RuleSet:
    name: str
    rules: list[str] = field(default_factory=list)
    config: dict[str, Any] = field(default_factory=dict)

    def to_linter_config(self) -> dict[str, Any]:
        return {"name": self.name, "rules": self.rules, **self.config}


# Curated rule sets per language ---------------------------------------------
PYTHON_RULES = RuleSet(
    name="python",
    rules=[
        "line-length=100",
        "target-version=py311",
        "select=E,F,W,I,N,B,UP,SIM,C4",
        "ignore=E501,S101",
    ],
    config={
        "ruff": {
            "line-length": 100,
            "target-version": "py311",
            "lint": {
                "select": ["E", "F", "W", "I", "N", "B", "UP", "SIM", "C4"],
                "ignore": ["E501", "S101"],
            },
        }
    },
)

JAVASCRIPT_RULES = RuleSet(
    name="javascript",
    rules=["semi", "no-unused-vars", "no-undef", "prefer-const", "eqeqeq"],
    config={"eslint": {"extends": "eslint:recommended"}},
)

RUST_RULES = RuleSet(
    name="rust",
    rules=["clippy::all", "clippy::pedantic", "clippy::nursery"],
    config={"clippy": {"all": True, "pedantic": True}},
)

GO_RULES = RuleSet(
    name="go",
    rules=["gofmt", "golint", "go vet", "errcheck"],
    config={"golangci-lint": {"enable": ["gofmt", "golint", "govet", "errcheck"]}},
)

WEB_RULES = RuleSet(
    name="web",
    rules=["prettier", "no-inline-styles", "accessibility-first"],
    config={"prettier": {"printWidth": 100, "tabWidth": 2}},
)

RULESETS: dict[str, RuleSet] = {
    "python": PYTHON_RULES,
    "javascript": JAVASCRIPT_RULES,
    "typescript": JAVASCRIPT_RULES,
    "rust": RUST_RULES,
    "go": GO_RULES,
    "web": WEB_RULES,
}


def ruleset_for(language: str) -> RuleSet:
    """Return the rule set for a language, defaulting to a generic set."""
    return RULESETS.get(language.lower(), RuleSet(name=language, rules=list(PRINCIPLES)))


def apply_principles(code: str) -> str:
    """Annotate code with a header summarizing the core principles."""
    header = "# Applied CODING_AI principles:\n" + "\n".join(
        f"# - {p}" for p in PRINCIPLES
    )
    return f"{header}\n{code}"
