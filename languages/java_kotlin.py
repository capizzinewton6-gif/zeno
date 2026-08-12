"""Maven/Gradle integration, JVM inspection, and static checks."""
from __future__ import annotations

from languages.base import ExecResult, LanguageEngine, LintResult


class JavaKotlinEngine(LanguageEngine):
    name = "java"
    extensions = (".java", ".kt", ".kts")

    def required_tools(self) -> list[str]:
        return ["java", "mvn", "gradle", "kotlinc"]

    def is_kotlin(self, path: str) -> bool:
        return path.endswith((".kt", ".kts"))

    def build_tool(self) -> str | None:
        return self._bin("gradle") or self._bin("mvn")

    def lint(self, path: str) -> LintResult:
        tool = self.build_tool()
        if not tool:
            return LintResult(ok=True, warnings=["no build tool installed"])
        if "gradle" in tool:
            result = self._exec(f"{tool} check --console=plain")
        else:
            result = self._exec(f"{tool} check")
        return LintResult(ok=result.ok, errors=result.stderr.splitlines()[-20:] if not result.ok else [])

    def format(self, path: str) -> LintResult:
        # spotless / ktfmt hooks
        tool = self._bin("gradle")
        if tool:
            result = self._exec(f"{tool} spotlessApply --console=plain")
            return LintResult(ok=result.ok, errors=[result.stderr] if result.stderr else [])
        return LintResult(ok=True, warnings=["no formatter available"])

    def run(self, path: str) -> ExecResult:
        if self.is_kotlin(path):
            kotlinc = self._bin("kotlinc")
            if not kotlinc:
                return ExecResult(False, -1, "", "kotlinc not installed")
            jar = path.rsplit(".", 1)[0] + ".jar"
            compile_res = self._exec(f"{kotlinc} {path} -include-runtime -d {jar}")
            if not compile_res.ok:
                return compile_res
            return self._exec(f"java -jar {jar}")
        # Java
        java = self._bin("java")
        javac = self._bin("javac")
        if not (java and javac):
            return ExecResult(False, -1, "", "java/javac not installed")
        cls = path.rsplit(".", 1)[0]
        compile_res = self._exec(f"{javac} {path}")
        if not compile_res.ok:
            return compile_res
        return self._exec(f"{java} {cls}")

    def jvm_inspect(self) -> ExecResult:
        java = self._bin("java")
        if not java:
            return ExecResult(False, -1, "", "java not installed")
        return self._exec(f"{java} -version")
