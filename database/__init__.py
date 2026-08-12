"""database package — SQLite databases for chemicals, reactions, spectra, safety, catalysts/solvents."""

from .init_db import init_all

__all__ = ["init_all"]
