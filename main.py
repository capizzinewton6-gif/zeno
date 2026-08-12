"""Main entry point for the Chemistry AI web application.

A Flask-based text-GUI that exposes the full capability catalog and runs
all simulations on the user interface. Uses Google Gemini 2.5 Flash (deep
reasoning) and Gemini 1.5 Flash (fast processing) exclusively.
"""

import os
import sys
import json
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify, send_from_directory

import ui
from setup import setup_check
from database import init_all
from database.queries import (search_chemical, search_reaction, search_spectrum,
                              search_hazard, list_solvents)
from calculations.stoichiometry import Stoichiometry
from calculations.thermodynamics import Thermodynamics
from calculations.kinetics import Kinetics
from calculations.equilibrium import Equilibrium
from calculations.electrochemistry import Electrochemistry
from calculations.spectroscopy_math import SpectroscopyMath
from calculations.quantum_math import QuantumMath
from calculations.unit_converter import UnitConverter
from tools.plot_generator import PlotGenerator
from tools.reaction_drawer import ReactionDrawer
from tools.formula_engine import FormulaEngine
from tools.cheminformatics import Cheminformatics
from chemical_safety_hazards.ghs_classifier import GHSClassifier
from chemical_safety_hazards.compatibility_checker import CompatibilityChecker

HERE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(HERE, "templates"),
            static_folder=os.path.join(HERE, "static"))
app.config["JSON_SORT_KEYS"] = False

plotter = PlotGenerator()
drawer = ReactionDrawer()
cheminfo = Cheminformatics()
ghs = GHSClassifier()
compat = CompatibilityChecker()

stoich, thermo, kin, eq, electro, spec, qm, uc = (Stoichiometry(), Thermodynamics(),
                                                   Kinetics(), Equilibrium(),
                                                   Electrochemistry(), SpectroscopyMath(),
                                                   QuantumMath(), UnitConverter())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "app": "Chemistry AI", "version": "1.0.0"})


@app.route("/api/capabilities")
def capabilities():
    return jsonify({"capabilities": ui.list_capabilities(), "count": len(ui.list_capabilities())})


@app.route("/api/engines")
def engines():
    return jsonify(ui.get_engines_info())


@app.route("/api/setup")
def setup_status():
    return jsonify(setup_check())


@app.route("/api/agent", methods=["POST"])
def agent_task():
    data = request.get_json(force=True) or {}
    task = data.get("task", "")
    params = data.get("params", {}) or {}
    result = ui.run_task(task, params)
    return jsonify(_jsonify(result))


@app.route("/api/stoichiometry", methods=["POST"])
def api_stoichiometry():
    d = request.get_json(force=True) or {}
    op = d.get("op")
    try:
        if op == "mass_to_moles":
            return jsonify({"result": stoich.mass_to_moles(float(d["mass_g"]), float(d["mm"]))})
        if op == "moles_to_mass":
            return jsonify({"result": stoich.moles_to_mass(float(d["moles"]), float(d["mm"]))})
        if op == "molarity":
            return jsonify({"result": stoich.molarity(float(d["moles"]), float(d["volume_L"]))})
        if op == "dilution":
            return jsonify({"result": stoich.dilution(float(d["c1"]), float(d["v1"]), float(d["c2"]))})
        if op == "percent_yield":
            return jsonify({"result": stoich.percent_yield(float(d["actual"]), float(d["theoretical"]))})
        if op == "limiting_reagent":
            return jsonify({"result": stoich.limiting_reagent(d["reactants"])})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"error": "unknown op"}), 400


@app.route("/api/thermodynamics", methods=["POST"])
def api_thermo():
    d = request.get_json(force=True) or {}
    op = d.get("op")
    try:
        if op == "gibbs":
            return jsonify({"result": thermo.gibbs_free_energy(float(d["dH"]), float(d["dS"]), float(d["T"]))})
        if op == "gibbs_from_K":
            return jsonify({"result": thermo.gibbs_from_equilibrium(float(d["K"]), float(d["T"]))})
        if op == "van_t_hoff":
            return jsonify({"result": thermo.van_t_hoff(float(d["K1"]), float(d["T1"]), float(d["T2"]), float(d["dH_J"]))})
        if op == "heat":
            return jsonify({"result": thermo.heat_transferred(float(d["m"]), float(d["c"]), float(d["dT"]))})
        if op == "calorimetry":
            return jsonify({"result": thermo.enthalpy_from_calorimetry(float(d["m"]), float(d["c"]), float(d["dT"]), float(d["moles"]))})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"error": "unknown op"}), 400


@app.route("/api/kinetics", methods=["POST"])
def api_kinetics():
    d = request.get_json(force=True) or {}
    op = d.get("op")
    try:
        if op == "arrhenius":
            return jsonify({"result": kin.arrhenius_rate(float(d["A"]), float(d["Ea"]), float(d["T"]))})
        if op == "half_life":
            return jsonify({"result": kin.half_life(int(d["order"]), float(d["k"]), float(d.get("C0", 1)))})
        if op == "rate_law":
            return jsonify({"result": kin.rate_law(d["concs"], float(d["k"]), d["orders"])})
        if op == "determine_order":
            return jsonify({"result": kin.determine_order(d["pairs"])})
        if op == "activation_energy":
            return jsonify({"result": kin.activation_energy_from_rates(float(d["k1"]), float(d["T1"]), float(d["k2"]), float(d["T2"]))})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"error": "unknown op"}), 400


@app.route("/api/equilibrium", methods=["POST"])
def api_equilibrium():
    d = request.get_json(force=True) or {}
    op = d.get("op")
    try:
        if op == "ph_from_h":
            return jsonify({"result": eq.ph_from_h(float(d["h"]))})
        if op == "weak_acid_ph":
            return jsonify({"result": eq.weak_acid_ph(float(d["ka"]), float(d["C"]))})
        if op == "weak_base_ph":
            return jsonify({"result": eq.weak_base_ph(float(d["kb"]), float(d["C"]))})
        if op == "henderson":
            return jsonify({"result": eq.henderson_hasselbalch(float(d["pka"]), float(d["base"]), float(d["acid"]))})
        if op == "pka":
            return jsonify({"result": eq.pka_from_ka(float(d["ka"]))})
        if op == "solubility":
            return jsonify({"result": eq.molar_solubility_from_ksp(float(d["ksp"]), d["coeffs"])})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"error": "unknown op"}), 400


@app.route("/api/electrochemistry", methods=["POST"])
def api_electro():
    d = request.get_json(force=True) or {}
    op = d.get("op")
    try:
        if op == "cell_potential":
            return jsonify({"result": electro.cell_potential(float(d["Ec"]), float(d["Ea"]))})
        if op == "nernst":
            return jsonify({"result": electro.nernst(float(d["E0"]), int(d["n"]), float(d["Q"]), float(d.get("T", 298.15)))})
        if op == "nernst_25c":
            return jsonify({"result": electro.nernst_25c(float(d["E0"]), int(d["n"]), float(d["Q"]))})
        if op == "gibbs":
            return jsonify({"result": electro.gibbs_from_potential(float(d["E"]), int(d["n"]))})
        if op == "faraday_mass":
            return jsonify({"result": electro.mass_deposited(float(d["I"]), float(d["t"]), float(d["mm"]), int(d["n"]))})
        if op == "equilibrium_K":
            return jsonify({"result": electro.equilibrium_constant(float(d["E0"]), int(d["n"]))})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"error": "unknown op"}), 400


@app.route("/api/spectroscopy", methods=["POST"])
def api_spectro():
    d = request.get_json(force=True) or {}
    op = d.get("op")
    try:
        if op == "beer_conc":
            return jsonify({"result": spec.beer_lambert_concentration(float(d["A"]), float(d["eps"]), float(d["b"]))})
        if op == "beer_abs":
            return jsonify({"result": spec.beer_lambert_absorbance(float(d["C"]), float(d["eps"]), float(d["b"]))})
        if op == "abs_from_T":
            return jsonify({"result": spec.absorbance_from_transmittance(float(d["T"]))})
        if op == "chemical_shift":
            return jsonify({"result": spec.chemical_shift_ppm(float(d["Hz"]), float(d["MHz"]))})
        if op == "mz":
            return jsonify({"result": spec.mass_to_charge(float(d["mass"]), int(d["charge"]))})
        if op == "energy_wavelength":
            return jsonify({"result": spec.energy_from_wavelength(float(d["nm"]))})
        if op == "wavenumber":
            return jsonify({"result": spec.wavenumber_from_wavelength(float(d["nm"]))})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"error": "unknown op"}), 400


@app.route("/api/quantum", methods=["POST"])
def api_quantum():
    d = request.get_json(force=True) or {}
    op = d.get("op")
    try:
        if op == "hydrogen_energy":
            return jsonify({"result": qm.hydrogen_energy_n(int(d["n"]))})
        if op == "particle_in_box":
            return jsonify({"result": qm.particle_in_box_energy(int(d["n"]), float(d["L"]))})
        if op == "harmonic":
            return jsonify({"result": qm.harmonic_oscillator_energy(int(d["n"]), float(d["omega"]))})
        if op == "gaussian_overlap":
            return jsonify({"result": qm.gaussian_overlap(float(d["alpha"]), float(d["beta"]), float(d["R"]))})
        if op == "hartree_to_ev":
            return jsonify({"result": qm.hartree_to_ev(float(d["hartree"]))})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"error": "unknown op"}), 400


@app.route("/api/units", methods=["POST"])
def api_units():
    d = request.get_json(force=True) or {}
    op = d.get("op")
    conv = {
        "c_to_f": ("c_to_f", ["c"]), "f_to_c": ("f_to_c", ["f"]),
        "c_to_k": ("c_to_k", ["c"]), "k_to_c": ("k_to_c", ["k"]),
        "atm_to_kpa": ("atm_to_kpa", ["atm"]), "kpa_to_atm": ("kpa_to_atm", ["kpa"]),
        "atm_to_mmhg": ("atm_to_mmhg", ["atm"]), "mmhg_to_atm": ("mmhg_to_atm", ["mmhg"]),
        "kj_to_kcal": ("kj_to_kcal", ["kj"]), "kcal_to_kj": ("kcal_to_kj", ["kcal"]),
        "ev_to_kjmol": ("ev_to_kj_mol", ["ev"]), "kjmol_to_ev": ("kj_mol_to_ev", ["kjmol"]),
        "ml_to_l": ("ml_to_l", ["ml"]), "l_to_ml": ("l_to_ml", ["l"]),
        "nm_to_angstrom": ("nm_to_angstrom", ["nm"]),
        "bohr_to_angstrom": ("bohr_to_angstrom", ["bohr"]),
    }
    if op not in conv:
        return jsonify({"error": "unknown op"}), 400
    method, args = conv[op]
    fn = getattr(uc, method)
    try:
        vals = [float(d[a]) for a in args]
        return jsonify({"result": fn(*vals)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/formula", methods=["POST"])
def api_formula():
    d = request.get_json(force=True) or {}
    f = d.get("formula", "")
    try:
        return jsonify({
            "formula": f,
            "monoisotopic_mass": FormulaEngine.monoisotopic_mass(f),
            "average_mass": FormulaEngine.average_mass(f),
            "isotopic_distribution": FormulaEngine.isotopic_distribution(f),
            "degree_of_unsaturation": FormulaEngine.degree_of_unsaturation(f),
            "percent_composition": FormulaEngine.percent_composition(f),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/cheminformatics", methods=["POST"])
def api_cheminfo():
    d = request.get_json(force=True) or {}
    op = d.get("op")
    try:
        if op == "parse_smiles":
            return jsonify(cheminfo.parse_smiles(d.get("smiles", "")))
        if op == "substructure":
            return jsonify(cheminfo.substructure_match(d.get("smiles", ""), d.get("smarts", "")))
        if op == "fingerprint":
            return jsonify(cheminfo.morgan_fingerprint(d.get("smiles", "")))
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"error": "unknown op"}), 400


@app.route("/api/plot/nmr", methods=["POST"])
def api_plot_nmr():
    d = request.get_json(force=True) or {}
    peaks = d.get("peaks", [[7.26, 1.0, "s"], [2.1, 3.0, "s"]])
    peaks = [(p[0], p[1], p[2] if len(p) > 2 else "") for p in peaks]
    result = plotter.nmr_spectrum(peaks, title=d.get("title", "Simulated 1H NMR"))
    return jsonify(_jsonify(result))


@app.route("/api/plot/chromatogram", methods=["POST"])
def api_plot_chromatogram():
    d = request.get_json(force=True) or {}
    peaks = d.get("peaks", [[3.1, 2.1e5, "product"]])
    peaks = [(p[0], p[1], p[2] if len(p) > 2 else "") for p in peaks]
    result = plotter.chromatogram(peaks, title=d.get("title", "Simulated HPLC"))
    return jsonify(_jsonify(result))


@app.route("/api/plot/kinetics", methods=["POST"])
def api_plot_kinetics():
    d = request.get_json(force=True) or {}
    result = plotter.kinetic_curve(d.get("times", []), d.get("concs", []),
                                   title=d.get("title", "Kinetic Decay"))
    return jsonify(_jsonify(result))


@app.route("/api/plot/calibration", methods=["POST"])
def api_plot_calib():
    d = request.get_json(force=True) or {}
    result = plotter.calibration_curve(d.get("x", []), d.get("y", []),
                                       title=d.get("title", "Calibration Curve"))
    return jsonify(_jsonify(result))


@app.route("/api/reaction_scheme", methods=["POST"])
def api_reaction_scheme():
    d = request.get_json(force=True) or {}
    result = drawer.draw_scheme(d.get("reactants", []), d.get("products", []),
                                conditions=d.get("conditions", ""), title=d.get("title", "Reaction Scheme"))
    return jsonify(_jsonify(result))


@app.route("/api/safety/ghs", methods=["POST"])
def api_ghs():
    d = request.get_json(force=True) or {}
    return jsonify(ghs.classify(d.get("chemical", "")))


@app.route("/api/safety/compatibility", methods=["POST"])
def api_compat():
    d = request.get_json(force=True) or {}
    return jsonify(compat.check_mixture(d.get("chemicals", [])))


@app.route("/api/db/search", methods=["POST"])
def api_db_search():
    d = request.get_json(force=True) or {}
    db = d.get("db")
    q = d.get("query", "")
    try:
        if db == "chemicals":
            return jsonify({"results": search_chemical(q)})
        if db == "reactions":
            return jsonify({"results": search_reaction(q)})
        if db == "spectra":
            return jsonify({"results": search_spectrum(q)})
        if db == "safety":
            return jsonify({"results": search_hazard(q)})
        if db == "solvents":
            return jsonify({"results": list_solvents()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"error": "unknown db"}), 400


@app.route("/api/init_db", methods=["POST"])
def api_init_db():
    return jsonify(init_all())


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory(app.static_folder, path)


def _jsonify(obj):
    """Recursively convert non-serializable objects for JSON response."""
    if isinstance(obj, dict):
        return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonify(v) for v in obj]
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, set):
        return [_jsonify(v) for v in obj]
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        return str(obj)


def run(host="0.0.0.0", port=12000, debug=False):
    """Start the Chemistry AI web application."""
    print("=" * 60)
    print("  Chemistry AI — Autonomous AI Chemistry Laboratory Assistant")
    print("  All simulations are performed on the user interface.")
    print("  Engines: Google Gemini 2.5 Flash (deep) + 1.5 Flash (fast)")
    print("=" * 60)
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 12000))
    run(port=port, debug=os.environ.get("FLASK_DEBUG", "0") == "1")
