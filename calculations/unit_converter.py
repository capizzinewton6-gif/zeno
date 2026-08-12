"""Unit converter — chemical unit conversions."""

import math


class UnitConverter:
    """Chemistry unit conversions."""

    @staticmethod
    def c_to_f(celsius):
        return celsius * 9.0 / 5.0 + 32.0

    @staticmethod
    def f_to_c(fahrenheit):
        return (fahrenheit - 32.0) * 5.0 / 9.0

    @staticmethod
    def c_to_k(celsius):
        return celsius + 273.15

    @staticmethod
    def k_to_c(kelvin):
        return kelvin - 273.15

    # --- Pressure ------------------------------------------------------
    @staticmethod
    def atm_to_kpa(atm):
        return atm * 101.325

    @staticmethod
    def kpa_to_atm(kpa):
        return kpa / 101.325

    @staticmethod
    def atm_to_mmhg(atm):
        return atm * 760.0

    @staticmethod
    def mmhg_to_atm(mmhg):
        return mmhg / 760.0

    @staticmethod
    def bar_to_atm(bar):
        return bar / 1.01325

    # --- Energy --------------------------------------------------------
    @staticmethod
    def kj_to_kcal(kj):
        return kj / 4.184

    @staticmethod
    def kcal_to_kj(kcal):
        return kcal * 4.184

    @staticmethod
    def ev_to_kj_mol(ev):
        return ev * 96.485

    @staticmethod
    def kj_mol_to_ev(kj_mol):
        return kj_mol / 96.485

    # --- Volume / concentration ----------------------------------------
    @staticmethod
    def ml_to_l(ml):
        return ml / 1000.0

    @staticmethod
    def l_to_ml(l):
        return l * 1000.0

    @staticmethod
    def m_to_mmol_l(M):
        return M * 1000.0

    @staticmethod
    def mg_l_to_ppm(mg_l, density=1.0):
        return mg_l / density

    # --- Length --------------------------------------------------------
    @staticmethod
    def nm_to_angstrom(nm):
        return nm * 10.0

    @staticmethod
    def angstrom_to_pm(angstrom):
        return angstrom * 100.0

    @staticmethod
    def cm_to_bohr(cm):
        return cm / 5.29177210903e-9

    @staticmethod
    def bohr_to_angstrom(bohr):
        return bohr * 0.529177210903
