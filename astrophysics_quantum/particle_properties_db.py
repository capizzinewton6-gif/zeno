"""PDG (Particle Data Group) particle masses, lifetimes, and spin-parity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class PDGParticle:
    name: str
    mass_MeV: float
    charge: float
    spin: float
    parity: int = 1
    lifetime_s: float = float("inf")
    quark_content: Optional[str] = None


# A compact subset of PDG values (masses in MeV/c^2).
PDG_DATA = {
    "electron": PDGParticle("electron", 0.51099895, -1, 0.5, 1, float("inf")),
    "muon": PDGParticle("muon", 105.6583755, -1, 0.5, 1, 2.1969811e-6),
    "tau": PDGParticle("tau", 1776.86, -1, 0.5, 1, 2.903e-13),
    "proton": PDGParticle("proton", 938.27208816, 1, 0.5, 1, float("inf"), "uud"),
    "neutron": PDGParticle("neutron", 939.56542052, 0, 0.5, 1, 879.4, "udd"),
    "pion_plus": PDGParticle("pi+", 139.57039, 1, 0, -1, 2.6033e-8, "u dbar"),
    "pion_zero": PDGParticle("pi0", 134.9768, 0, 0, -1, 8.4e-17, "(u ubar - d dbar)/sqrt2"),
    "kaon_plus": PDGParticle("K+", 493.677, 1, 0, -1, 1.238e-8, "u sbar"),
    "photon": PDGParticle("photon", 0.0, 0, 1, -1, float("inf")),
    "W": PDGParticle("W", 80377, 1, 1, -1, float("inf")),
    "Z": PDGParticle("Z", 91187.6, 0, 1, -1, float("inf")),
    "Higgs": PDGParticle("Higgs", 125250, 0, 0, 1, float("inf")),
}


class ParticlePropertiesDB:
    """Lookup table of PDG particle properties."""

    @staticmethod
    def get(name: str) -> PDGParticle:
        try:
            return PDG_DATA[name.lower()]
        except KeyError as exc:
            raise KeyError(f"Unknown particle: {name}. Known: {list(PDG_DATA)}") from exc

    @staticmethod
    def all_particles() -> dict[str, PDGParticle]:
        return dict(PDG_DATA)

    @staticmethod
    def decay_length(name: str, gamma: float = 1.0) -> float:
        from tools.constant_engine import CONSTANTS
        c = CONSTANTS.value("c")
        p = ParticlePropertiesDB.get(name)
        if p.lifetime_s == float("inf"):
            return float("inf")
        return p.lifetime_s * gamma * c
