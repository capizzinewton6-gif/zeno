"""Cargo package management, rustfmt, and borrow-checker tools."""
from __future__ import annotations

from languages.base import ExecResult, LanguageEngine, LintResult


class RustEngine(LanguageEngine):
    name = "rust"
    extensions = (".rs",)

    def required_tools(self) -> list[str]:
        return ["cargo", "rustc", "rustfmt"]

    def lint(self, path: str) -> LintResult:
        cargo = self._bin("cargo")
        if not cargo:
            return LintResult(ok=True, warnings=["cargo not installed"])
        result = self._exec(f"{cargo} clippy --message-format=short")
        errors, warnings = [], []
        for line in result.stdout.splitlines():
            if ": error" in line:
                errors.append(line)
            elif ": warning" in line:
                warnings.append(line)
        return LintResult(ok=result.ok, errors=errors, warnings=warnings)

    def format(self, path: str) -> LintResult:
        rustfmt = self._bin("rustfmt")
        if not rustfmt:
            return LintResult(ok=True, warnings=["rustfmt not installed"])
        result = self._exec(f"{rustfmt} {path}")
        return LintResult(ok=result.ok, errors=[result.stderr] if result.stderr else [])

    def run(self, path: str) -> ExecResult:
        cargo = self._bin("cargo")
        if cargo and path.endswith("Cargo.toml"):
            return self._exec(f"{cargo} run")
        rustc = self._bin("rustc")
        if rustc:
            out = path.replace(".rs", "")
            compile_res = self._exec(f"{rustc} {path} -o {out}")
            if not compile_res.ok:
                return compile_res
            return self._exec(f"./{out}")
        return ExecResult(False, -1, "", "no rust toolchain available")

    def check_borrow(self, path: str) -> LintResult:
        cargo = self._bin("cargo")
        if not cargo:
            return LintResult(ok=True, warnings=["cargo not installed"])
        result = self._exec(f"{cargo} check --message-format=short")
        return LintResult(ok=result.ok, errors=[l for l in result.stderr.splitlines() if "error" in l.lower()])
