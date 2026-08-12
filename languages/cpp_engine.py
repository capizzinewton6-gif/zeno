"""C/C++ memory checks, CMake configuration, and compiler hooks."""
from __future__ import annotations

from languages.base import ExecResult, LanguageEngine, LintResult


class CppEngine(LanguageEngine):
    name = "cpp"
    extensions = (".c", ".cpp", ".cc", ".h", ".hpp")

    def required_tools(self) -> list[str]:
        return ["gcc", "gpp", "cmake", "valgrind"]

    def compiler(self) -> str:
        return self._bin("gpp") or self._bin("g++") or self._bin("gcc") or "g++"

    def lint(self, path: str) -> LintResult:
        # Use compiler warnings as a lint pass
        cc = self.compiler()
        result = self._exec(f"{cc} -fsyntax-only -Wall -Wextra {path}")
        errors, warnings = [], []
        for line in result.stderr.splitlines():
            if "error:" in line:
                errors.append(line)
            elif "warning:" in line:
                warnings.append(line)
        return LintResult(ok=result.ok, errors=errors, warnings=warnings)

    def format(self, path: str) -> LintResult:
        clangfmt = self._bin("clang-format")
        if not clangfmt:
            return LintResult(ok=True, warnings=["clang-format not installed"])
        result = self._exec(f"{clangfmt} -i {path}")
        return LintResult(ok=result.ok, errors=[result.stderr] if result.stderr else [])

    def compile(self, path: str, output: str | None = None) -> ExecResult:
        cc = self.compiler()
        out = output or path.rsplit(".", 1)[0]
        return self._exec(f"{cc} {path} -o {out} -Wall -O2")

    def run(self, path: str) -> ExecResult:
        out = path.rsplit(".", 1)[0]
        compile_res = self.compile(path, out)
        if not compile_res.ok:
            return compile_res
        return self._exec(f"./{out}")

    def cmake_build(self, build_dir: str = "build") -> ExecResult:
        cmake = self._bin("cmake")
        if not cmake:
            return ExecResult(False, -1, "", "cmake not installed")
        return self._exec(f"{cmake} -B {build_dir} && {cmake} --build {build_dir}")

    def valgrind(self, binary: str) -> ExecResult:
        vg = self._bin("valgrind")
        if not vg:
            return ExecResult(False, -1, "", "valgrind not installed")
        return self._exec(f"{vg} --leak-check=full ./{binary}")
