"""Open-source dependency license compatibility verification."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# Permissive licenses are broadly compatible. Copyleft (GPL) has restrictions.
LICENSE = {
    "permissive": {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense", "MPL-2.0"},
    "copyleft": {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.1", "LGPL-3.0"},
    "public": {"CC0-1.0", "WTFPL"},
}


@dataclass
class LicenseEntry:
    name: str
    license: str
    category: str = "unknown"


@dataclass
class LicenseReport:
    entries: list[LicenseEntry] = field(default_factory=list)
    compatible: bool = True
    conflicts: list[str] = field(default_factory=list)

    @property
    def has_copyleft(self) -> bool:
        return any(e.category == "copyleft" for e in self.entries)


class LicenseChecker:
    """Checks license compatibility of dependencies."""

    SPDX_IDENTIFIERS = {lic for cat in LICENSE.values() for lic in cat}

    def categorize(self, license_str: str) -> str:
        s = license_str.strip()
        for cat, licenses in LICENSE.items():
            if s in licenses:
                return cat
        # Loose matching
        sup = s.upper()
        if "GPL" in sup or "AGPL" in sup:
            return "copyleft"
        if "MIT" in sup or "BSD" in sup or "APACHE" in sup or "ISC" in sup:
            return "permissive"
        return "unknown"

    def check(self, dependencies: list[dict[str, str]],
              project_license: str = "MIT") -> LicenseReport:
        report = LicenseReport()
        proj_cat = self.categorize(project_license)
        for dep in dependencies:
            cat = self.categorize(dep.get("license", ""))
            entry = LicenseEntry(name=dep.get("name", ""),
                                 license=dep.get("license", ""), category=cat)
            report.entries.append(entry)
            # Copyleft deps conflict with permissive project license
            if cat == "copyleft" and proj_cat == "permissive":
                report.compatible = False
                report.conflicts.append(
                    f"{entry.name} ({entry.license}) is copyleft; incompatible with {project_license}")
        return report

    def from_requirements(self, text: str) -> list[dict[str, str]]:
        """Best-effort: returns deps with unknown licenses (to be enriched)."""
        import re
        deps: list[dict[str, str]] = []
        for line in text.splitlines():
            m = re.match(r"^([A-Za-z0-9_.\-]+)", line.strip())
            if m:
                deps.append({"name": m.group(1), "license": "unknown"})
        return deps
