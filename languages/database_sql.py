"""SQL query optimizer, dialect converters, and ORM mapping."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from languages.base import ExecResult, LanguageEngine, LintResult


DIALECTS = ("postgres", "mysql", "sqlite", "mssql", "oracle")


@dataclass
class QueryAnalysis:
    dialect: str
    tables: list[str] = field(default_factory=list)
    joins: int = 0
    subqueries: int = 0
    has_wildcard_select: bool = False
    warnings: list[str] = field(default_factory=list)


class DatabaseSQLEngine(LanguageEngine):
    name = "sql"
    extensions = (".sql",)

    def required_tools(self) -> list[str]:
        return ["sqlite3"]

    def lint(self, path: str) -> LintResult:
        try:
            with open(path, encoding="utf-8") as f:
                sql = f.read()
        except OSError:
            return LintResult(ok=False, errors=["file not readable"])
        analysis = self.analyze(sql)
        return LintResult(ok=True, warnings=analysis.warnings)

    def format(self, path: str) -> LintResult:
        try:
            with open(path, encoding="utf-8") as f:
                sql = f.read()
        except OSError:
            return LintResult(ok=False, errors=["file not readable"])
        formatted = self.format_sql(sql)
        with open(path, "w", encoding="utf-8") as f:
            f.write(formatted)
        return LintResult(ok=True)

    def run(self, path: str) -> ExecResult:
        sqlite3 = self._bin("sqlite3")
        if not sqlite3:
            return ExecResult(False, -1, "", "sqlite3 not installed")
        return self._exec(f"{sqlite3} :memory: < {path}")

    def analyze(self, sql: str, dialect: str = "postgres") -> QueryAnalysis:
        tables = list(set(re.findall(r"\bfrom\s+(\w+)|\bjoin\s+(\w+)", sql, re.IGNORECASE)))
        tables = [t for pair in tables for t in pair if t]
        joins = len(re.findall(r"\bjoin\b", sql, re.IGNORECASE))
        subqueries = sql.lower().count("select") - 1
        wildcard = bool(re.search(r"select\s+\*", sql, re.IGNORECASE))
        warnings: list[str] = []
        if wildcard:
            warnings.append("SELECT * used; specify columns for performance")
        if subqueries > 2:
            warnings.append(f"{subqueries} subqueries; consider refactoring to joins")
        if not re.search(r"\bwhere\b", sql, re.IGNORECASE) and "delete" in sql.lower():
            warnings.append("DELETE without WHERE clause")
        return QueryAnalysis(dialect=dialect, tables=tables, joins=joins,
                             subqueries=max(0, subqueries),
                             has_wildcard_select=wildcard, warnings=warnings)

    def format_sql(self, sql: str) -> str:
        keywords = ("SELECT", "FROM", "WHERE", "JOIN", "INNER JOIN", "LEFT JOIN",
                    "RIGHT JOIN", "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "INSERT INTO",
                    "VALUES", "UPDATE", "SET", "DELETE FROM", "CREATE TABLE", "ALTER TABLE")
        out = sql
        for kw in keywords:
            out = re.sub(rf"\b{kw}\b", kw, out, flags=re.IGNORECASE)
        for kw in keywords:
            out = out.replace(kw, f"\n{kw}")
        return out.strip()

    def convert_dialect(self, sql: str, target: str) -> str:
        """Best-effort dialect conversion (handles common type/func differences)."""
        out = sql
        if target == "sqlite":
            out = re.sub(r"\bSERIAL\b", "INTEGER", out, flags=re.IGNORECASE)
            out = re.sub(r"\bBOOLEAN\b", "INTEGER", out, flags=re.IGNORECASE)
        elif target == "postgres":
            out = re.sub(r"\bAUTOINCREMENT\b", "SERIAL", out, flags=re.IGNORECASE)
        return out

    def to_orm(self, sql: str, framework: str = "sqlalchemy") -> str:
        """Sketch an ORM model from a CREATE TABLE statement (SQLAlchemy)."""
        tables = re.findall(r"CREATE TABLE\s+(\w+)\s*\((.*?)\);", sql, re.IGNORECASE | re.DOTALL)
        models: list[str] = ["from sqlalchemy import Column, Integer, String, Text\n",
                             "from sqlalchemy.orm import declarative_base\n\n",
                             "Base = declarative_base()\n\n"]
        for name, body in tables:
            cls = "".join(w.capitalize() for w in name.split("_"))
            models.append(f"class {cls}(Base):\n    __tablename__ = \"{name}\"\n")
            for col_line in body.split(","):
                col_line = col_line.strip()
                if not col_line:
                    continue
                m = re.match(r"(\w+)\s+(\w+)", col_line)
                if m:
                    col_name, col_type = m.group(1), m.group(2).upper()
                    py_type = "Integer" if "INT" in col_type else "String"
                    models.append(f"    {col_name} = Column({py_type})\n")
            models.append("\n")
        return "".join(models)
