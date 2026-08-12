"""Spectroscopy math — Beer-Lambert law, chemical shift, and mass-to-charge ratios."""

import math


class SpectroscopyMath:
    """Spectroscopic calculations."""

    SPEED_OF_LIGHT = 2.998e8  # m/s
    PLANCK = 6.626e-34        # J*s
    AVOGADRO = 6.022e23

    # --- Beer-Lambert --------------------------------------------------
    @staticmethod
    def absorbance_from_transmittance(T):
        return -math.log10(T)

    @staticmethod
    def transmittance_from_absorbance(A):
        return 10 ** (-A)

    @staticmethod
    def beer_lambert_concentration(A, epsilon, path_length_cm):
        return A / (epsilon * path_length_cm)

    @staticmethod
    def beer_lambert_absorbance(concentration_M, epsilon, path_length_cm):
        return epsilon * path_length_cm * concentration_M

    @staticmethod
    def molar_absorptivity(A, concentration_M, path_length_cm):
        return A / (concentration_M * path_length_cm)

    # --- NMR chemical shift --------------------------------------------
    @staticmethod
    def larmor_frequency(field_T, gamma_MHz_per_T=42.577):
        """gamma for 1H ~ 42.577 MHz/T."""
        return field_T * gamma_MHz_per_T

    @staticmethod
    def chemical_shift_ppm(observed_Hz, spectrometer_MHz):
        return (observed_Hz / spectrometer_MHz)

    # --- Mass spectrometry --------------------------------------------
    @staticmethod
    def mass_to_charge(mass_Da, charge):
        return mass_Da / charge

    @staticmethod
    def isotope_pattern(monoisotopic_mass, n_carbons=1, c13_abund=0.0107):
        """Approximate M+1 isotope abundance from 13C natural abundance."""
        return {"M": 1.0, "M+1": n_carbons * c13_abund}

    # --- IR / general wave conversions --------------------------------
    @staticmethod
    def wavenumber_from_wavelength(wavelength_nm):
        """cm^-1 = 1e7 / wavelength(nm)."""
        return 1e7 / wavelength_nm

    @staticmethod
    def energy_from_wavelength(wavelength_nm):
        """E (J) = hc/lambda."""
        lam_m = wavelength_nm * 1e-9
        return (SpectroscopyMath.PLANCK * SpectroscopyMath.SPEED_OF_LIGHT) / lam_m

    @staticmethod
    def energy_from_wavenumber(wavenumber_cm):
        lam_m = 1e-2 / wavenumber_cm
        return (SpectroscopyMath.PLANCK * SpectroscopyMath.SPEED_OF_LIGHT) / lam_m
