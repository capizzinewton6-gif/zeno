"""ui module — User interface and interaction layer for Chemistry AI.

Wraps the ChemistryAgent into JSON-friendly actions used by the Flask app
in main.py. All simulations are performed on the user interface.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.chemistry_agent import ChemistryAgent
from database import init_all

_AGENT = None


def get_agent(api_key=None):
    global _AGENT
    if _AGENT is None:
        _AGENT = ChemistryAgent(api_key=api_key)
    return _AGENT


def reset_agent(api_key=None):
    global _AGENT
    _AGENT = ChemistryAgent(api_key=api_key)
    return _AGENT


def list_capabilities():
    """Return the full capability catalog for the UI."""
    return [
        {"module": "agents/chemistry_agent.py", "capability": "Main chemical intelligence & routing"},
        {"module": "agents/synthetic_agent.py", "capability": "Reaction pathways & retrosynthesis"},
        {"module": "agents/quantum_agent.py", "capability": "Ab initio electronic structure"},
        {"module": "agents/analytical_agent.py", "capability": "Spectroscopy & chromatography interpretation"},
        {"module": "agents/research_agent.py", "capability": "Literature & database research"},
        {"module": "agents/optimization_agent.py", "capability": "Condition & stoichiometry optimization"},
        {"module": "agents/project_agent.py", "capability": "Synthesis & materials project management"},
        {"module": "synthesis/retrosynthesis_engine.py", "capability": "Disconnection & precursor planning"},
        {"module": "synthesis/reaction_planner.py", "capability": "Reagents, solvents, catalyst selection"},
        {"module": "synthesis/yield_predictor.py", "capability": "Yield & side-product prediction"},
        {"module": "synthesis/protecting_groups.py", "capability": "Protection/deprotection strategy"},
        {"module": "synthesis/stereocontrol_planner.py", "capability": "Asymmetric synthesis & resolution"},
        {"module": "synthesis/purification_planner.py", "capability": "Chromatography, recrystallization, distillation"},
        {"module": "synthesis/scaleup_calculator.py", "capability": "Process scale-up & runaway risk"},
        {"module": "calculations/stoichiometry.py", "capability": "Moles, molarity, limiting reagents, % yield"},
        {"module": "calculations/thermodynamics.py", "capability": "Hess's Law, van 't Hoff, heat capacity"},
        {"module": "calculations/kinetics.py", "capability": "Rate laws, Arrhenius, reaction order"},
        {"module": "calculations/equilibrium.py", "capability": "Ka, Kb, Ksp, pH, buffer capacity"},
        {"module": "calculations/electrochemistry.py", "capability": "Nernst, reduction potentials, Faraday's laws"},
        {"module": "calculations/spectroscopy_math.py", "capability": "Beer-Lambert, chemical shift, m/z"},
        {"module": "calculations/quantum_math.py", "capability": "Schrodinger matrix elements & basis sets"},
        {"module": "calculations/unit_converter.py", "capability": "Chemical unit conversions"},
        {"module": "lab_automation/synthesis_robot.py", "capability": "Automated liquid/solid & flow control"},
        {"module": "lab_automation/sensor_calibration.py", "capability": "pH, thermocouple, pressure calibration"},
        {"module": "lab_automation/instrument_interface.py", "capability": "GC-MS, HPLC, NMR, UV-Vis interface"},
        {"module": "lab_automation/data_acquisition.py", "capability": "Real-time T/P/absorbance acquisition"},
        {"module": "lab_automation/error_analysis.py", "capability": "Drift, calibration curves, SNR"},
        {"module": "lab_automation/safety_interlocks.py", "capability": "Fume hood, thermal runaway, gas leak"},
        {"module": "prototyping/experiment_builder.py", "capability": "Wet-lab protocols & benchtop procedures"},
        {"module": "prototyping/reactor_setup.py", "capability": "Schlenk, autoclave, flow, reflux setups"},
        {"module": "prototyping/chromatography_builder.py", "capability": "HPLC/GC column & mobile phase selection"},
        {"module": "prototyping/electronics_interface.py", "capability": "MFC & heating mantle integration"},
        {"module": "prototyping/bill_of_materials.py", "capability": "Chemical inventory & CAS registry"},
        {"module": "prototyping/execution_planner.py", "capability": "SOPs & batch logs"},
        {"module": "materials_chemistry/polymer_db.py", "capability": "Mn, Mw, PDI, Tg"},
        {"module": "materials_chemistry/mof_frameworks.py", "capability": "MOF pore volume & BET surface area"},
        {"module": "materials_chemistry/nanomaterial_properties.py", "capability": "QD bandgaps & NP functionalization"},
        {"module": "materials_chemistry/catalyst_design.py", "capability": "Active sites, TOF, adsorption energy"},
        {"module": "materials_chemistry/material_selector.py", "capability": "Precursor, binder, dopant selection"},
        {"module": "chemical_safety_hazards/ghs_classifier.py", "capability": "GHS hazard classes & pictograms"},
        {"module": "chemical_safety_hazards/msds_generator.py", "capability": "SDS & exposure limits (PEL/TLV)"},
        {"module": "chemical_safety_hazards/compatibility_checker.py", "capability": "Reactivity & hazardous mixture prevention"},
        {"module": "chemical_safety_hazards/toxicity_screening.py", "capability": "QSAR toxicity & bioaccumulation"},
        {"module": "chemical_safety_hazards/waste_disposal.py", "capability": "Solvent segregation & neutralization"},
        {"module": "research/pubchem_search.py", "capability": "PubChem, ChemSpider, CAS query"},
        {"module": "research/reaction_search.py", "capability": "Reaction database search"},
        {"module": "research/paper_reader.py", "capability": "Parse ACS/RSC/Wiley papers"},
        {"module": "research/patent_search.py", "capability": "Composition & process patent search"},
        {"module": "research/reference_manager.py", "capability": "BibTeX & reaction citations"},
        {"module": "project/research_manager.py", "capability": "Research project & target management"},
        {"module": "project/task_manager.py", "capability": "Synthesis/characterization task tracking"},
        {"module": "project/notebook_manager.py", "capability": "Electronic Lab Notebook (ELN)"},
        {"module": "project/documentation.py", "capability": "1H NMR/HRMS characterization lists"},
        {"module": "project/paper_generator.py", "capability": "Publication-ready ACS manuscripts"},
        {"module": "tools/cheminformatics.py", "capability": "SMILES parsing, substructure, fingerprints"},
        {"module": "tools/plot_generator.py", "capability": "NMR/chromatogram/kinetic plots"},
        {"module": "tools/reaction_drawer.py", "capability": "Reaction schemes & figures"},
        {"module": "tools/formula_engine.py", "capability": "Exact mass, MW, isotopic distributions"},
        {"module": "tools/file_manager.py", "capability": "MOL/SDF/CIF/JCAMP-DX/FID files"},
        {"module": "tools/data_analyzer.py", "capability": "LC-MS integration & plate kinetics"},
        {"module": "ai_core/ai_engine.py", "capability": "Main AI intelligence"},
        {"module": "ai_core/reasoning_engine.py", "capability": "Mechanistic & thermochemical reasoning"},
        {"module": "ai_core/planning_engine.py", "capability": "Multi-step synthesis planning"},
        {"module": "ai_core/context_manager.py", "capability": "Reaction context (pH, T, solvent)"},
        {"module": "ai_core/knowledge_engine.py", "capability": "Chemical ontology & reaction graph"},
        {"module": "ai_core/safety_layer.py", "capability": "Dual-use & precursor screening"},
        {"module": "src/gemini_25_flash_engine", "capability": "Advanced reasoning (Gemini 2.5 Flash)"},
        {"module": "src/gemini_15_flash_engine", "capability": "Fast processing (Gemini 1.5 Flash)"},
    ]


def run_task(task, params=None, api_key=None):
    """Execute a chemistry task through the ChemistryAgent."""
    agent = get_agent(api_key=api_key)
    return agent.handle({"task": task, "params": params or {}})


def ensure_databases():
    return init_all()


def get_engines_info():
    from src.gemini_25_flash_engine import describe as d25
    from src.gemini_15_flash_engine import describe as d15
    return {"deep_reasoning": d25(), "fast_processing": d15()}
