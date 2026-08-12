"""Package audit, dependency upgrades, and lockfile parsers."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from capabilities.terminal_execution import CommandResult, TerminalExecution


@dataclass
class Dependency:
    name: str
    version: str
    latest: str = ""
    vulnerable: bool = False
    dev: bool = False


@dataclass
class AuditReport:
    manager: str
    total: int = 0
    outdated: list[Dependency] = field(default_factory=list)
    vulnerable: list[Dependency] = field(default_factory=list)


class DependencyManager:
    """Audits and upgrades dependencies across package managers."""

    def __init__(self, terminal: TerminalExecution | None = None,
                 workspace: str = ".") -> None:
        self.terminal = terminal or TerminalExecution(workspace=workspace)
        self.workspace = workspace

    def detect_manager(self) -> str | None:
        p = Path(self.workspace)
        if (p / "pyproject.toml").exists() or (p / "requirements.txt").exists():
            return "pip"
        if (p / "package.json").exists():
            return "npm"
        if (p / "Cargo.toml").exists():
            return "cargo"
        if (p / "go.mod").exists():
            return "go"
        return None

    def audit(self) -> AuditReport:
        mgr = self.detect_manager()
        if mgr == "pip":
            return self._audit_pip()
        if mgr == "npm":
            return self._audit_npm()
        return AuditReport(manager=mgr or "unknown")

    def upgrade(self, names: list[str] | None = None) -> CommandResult:
        mgr = self.detect_manager()
        if mgr == "pip":
            pkgs = " ".join(names) if names else "-r requirements.txt"
            return self.terminal.run(f"pip install --upgrade {pkgs}")
        if mgr == "npm":
            pkgs = " ".join(names) if names else ""
            return self.terminal.run(f"npm update {pkgs}".strip())
        if mgr == "cargo":
            return self.terminal.run("cargo update")
        if mgr == "go":
            return self.terminal.run("go get -u ./...")
        return CommandResult("", -1, "", f"no manager detected in {self.workspace}")

    def parse_lockfile(self) -> dict[str, str]:
        """Parse the relevant lockfile into a name->version map."""
        p = Path(self.workspace)
        if (p / "package-lock.json").exists():
            return self._parse_npm_lock(p / "package-lock.json")
        if (p / "requirements.txt").exists():
            return self._parse_requirements(p / "requirements.txt")
        if (p / "Cargo.lock").exists():
            return self._parse_cargo_lock(p / "Cargo.lock")
        return {}

    def _audit_pip(self) -> AuditReport:
        res = self.terminal.run("pip-audit -f json", timeout=60)
        report = AuditReport(manager="pip")
        if res.ok and res.stdout:
            try:
                data = json.loads(res.stdout)
                for dep in data.get("dependencies", []):
                    d = Dependency(name=dep.get("name", ""), version=dep.get("version", ""),
                                   vulnerable=bool(dep.get("vulns")))
                    report.vulnerable.append(d) if d.vulnerable else None
                    report.total += 1
            except json.JSONDecodeError:
                pass
        return report

    def _audit_npm(self) -> AuditReport:
        res = self.terminal.run("npm audit --json", timeout=60)
        report = AuditReport(manager="npm")
        if res.stdout:
            try:
                data = json.loads(res.stdout)
                report.total = data.get("metadata", {}).get("totalDependencies", 0)
                for name, info in data.get("vulnerabilities", {}).items():
                    report.vulnerable.append(
                        Dependency(name=name, version=info.get("via", ""),
                                   vulnerable=True))
            except json.JSONDecodeError:
                pass
        return report

    def _parse_npm_lock(self, path: Path) -> dict[str, str]:
        data = json.loads(path.read_text(encoding="utf-8"))
        out: dict[str, str] = {}
        for name, info in data.get("packages", {}).items():
            if name:
                out[name] = info.get("version", "")
        return out

    def _parse_requirements(self, path: Path) -> dict[str, str]:
        out: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^([^=<>!~]+)[=<>!~]+([\w.]+)", line.strip())
            if m:
                out[m.group(1).strip()] = m.group(2)
        return out

    def _parse_cargo_lock(self, path: Path) -> dict[str, str]:
        out: dict[str, str] = {}
        name = version = None
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("name = "):
                name = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("version = "):
                version = line.split("=", 1)[1].strip().strip('"')
                if name:
                    out[name] = version or ""
                    name = None
        return out
