# ⚗️ Zeno — Chemistry AI

An advanced **text-GUI-based AI Chemistry Laboratory Assistant** that functions as an intelligent
research partner for students, educators, researchers, laboratory technicians, and professional
chemists. It understands high-level chemical instructions, decomposes complex problems, researches
relevant information, and solves advanced chemistry problems using rigorous scientific reasoning.

> **All simulations are performed on the user interface.**

## Architecture

Built on a **One Capability = One Source Code Module** architecture, where every chemistry feature is
an independent software component with its own codebase, configuration, documentation, and tests.

```
zeno/
├── main.py                  # Flask entry point (web UI + REST API)
├── ui.py                    # UI interaction layer
├── setup.py                 # Installation & configuration
├── agents/                  # 7 specialist orchestrating agents
├── ai_core/                 # AI engine, reasoning, planning, knowledge, safety
├── src/                     # Gemini engines (2.5 Flash deep, 1.5 Flash fast)
├── calculations/            # 8 calculation modules
├── tools/                   # 6 tool modules
├── synthesis/               # 7 synthesis modules
├── lab_automation/          # 6 lab automation modules
├── prototyping/             # 6 prototyping modules
├── materials_chemistry/     # 5 materials modules
├── chemical_safety_hazards/ # 5 safety modules
├── research/                # 5 research modules
├── project/                 # 5 project modules
├── database/                # 5 SQLite databases + init/query helpers
├── memory/                  # JSON memory stores
├── config/                  # settings, api_keys, paths
├── templates/               # Web UI
├── static/                  # Generated plots & schemes
└── requirements.txt
```

## AI Engines

Uses **Google Gemini 2.5 Flash** (advanced chemical reasoning) and **Gemini 1.5 Flash** (fast
document processing) exclusively. Set `GEMINI_API_KEY` to enable live reasoning; without it the
engines run in offline simulation mode (all simulations on the UI).

## Quick Start

```bash
pip install -r requirements.txt
python -m database.init_db      # initialize SQLite databases
python main.py                  # start the web app on port 12000
```

Then open `http://localhost:12000/` in your browser.

## Capabilities

68 capability modules spanning: stoichiometry, thermodynamics, kinetics, equilibrium, electrochemistry,
spectroscopy, quantum chemistry, cheminformatics, retrosynthesis, reaction planning, yield prediction,
protecting groups, stereocontrol, purification, scale-up, lab automation, prototyping, materials chemistry,
chemical safety (GHS/SDS/compatibility/toxicity/waste), research (PubChem/patents/papers), project
management (ELN/manuscripts), and more.

## Safety

The `ai_core/safety_layer.py` screens all requests for dual-use research, chemical weapons, and illicit
precursor synthesis and blocks disallowed content.
