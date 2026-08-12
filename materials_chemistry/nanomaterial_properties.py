"""Nanomaterial properties — quantum dot bandgaps and nanoparticle functionalization."""

import math


class NanomaterialProperties:
    """Quantum dot and nanoparticle calculations."""

    # Effective mass approximation parameters (CdSe example)
    @staticmethod
    def quantum_dot_bandgap(bulk_Eg_eV, radius_nm, exciton_bohr_radius_nm=5.6,
                            me_eff=0.13, mh_eff=0.45):
        """Brus equation: E = Eg + h^2*pi^2/(2*R^2)*(1/me+1/mh) - 1.8*e^2/(eps*R)."""
        hbar2 = 0.0381  # eV*nm^2 (hbar^2 in convenient units)
        confinement = (hbar2 * math.pi ** 2) / (2 * radius_nm ** 2) * (1.0 / me_eff + 1.0 / mh_eff)
        coulomb = 1.8 / (radius_nm * 10)  # simplified Coulomb term (eV)
        return round(bulk_Eg_eV + confinement - coulomb, 3)

    @staticmethod
    def nanoparticle_surface_atoms(radius_nm, lattice_constant_nm=0.4):
        """Fraction of atoms on the surface of a spherical nanoparticle."""
        n_total = (4.0 / 3.0) * math.pi * (radius_nm / lattice_constant_nm) ** 3
        n_surface = 4.0 * math.pi * (radius_nm / lattice_constant_nm) ** 2
        return {"total_atoms": round(n_total), "surface_atoms": round(n_surface),
                "surface_fraction": round(n_surface / n_total, 3) if n_total else 0}

    @staticmethod
    def ligand_density(surface_area_nm2, footprint_nm2=0.21):
        """Maximum ligand density (molecules/nm^2) for a given footprint."""
        return round(1.0 / footprint_nm2, 2)
