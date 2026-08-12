# Zeno — Chemistry AI

## Overview
Autonomous AI Chemistry Laboratory Assistant web app (Flask). Text-GUI based; all simulations on the UI.
Uses Google Gemini 2.5 Flash (deep reasoning) + 1.5 Flash (fast processing) exclusively.

## Run
```bash
pip install -r requirements.txt
python -m database.init_db        # init SQLite DBs (first run)
PORT=12000 python main.py         # web app on port 12000
```
External: https://work-1-zpbvndyqgmqgxjkp.prod-runtime.all-hands.dev/ (port 12000), work-2 on 12001.

## Architecture
One Capability = One Source Code Module. 68 capability modules + 7 agents.
- `main.py` — Flask app + REST API (`/api/*`)
- `ui.py` — UI interaction layer wrapping `agents.chemistry_agent.ChemistryAgent`
- `agents/` — 7 orchestrating agents (chemistry, synthetic, quantum, analytical, research, optimization, project)
- `ai_core/` — AI engine, reasoning, planning, context, knowledge, safety_layer
- `src/gemini_25_flash_engine`, `src/gemini_15_flash_engine` — Gemini engine stubs (offline fallback when no GEMINI_API_KEY)
- `calculations/`, `tools/`, `synthesis/`, `lab_automation/`, `prototyping/`, `materials_chemistry/`, `chemical_safety_hazards/`, `research/`, `project/` — capability packages
- `database/` — 5 SQLite DBs + `init_db.py` + `queries.py`
- `memory/` — JSON stores; `config/` — settings/api_keys/paths; `templates/index.html` — single-page UI

## Conventions
- Each capability module exposes a class with static/instance methods; agents orchestrate them.
- All agent `handle(request)` takes `{"task": str, "params": dict}` and returns a JSON-serializable dict.
- Numeric params may arrive as strings (from UI) — coerce with float() in agents.
- Safety: `ai_core/safety_layer.py` blocks disallowed keywords (nerve agents, weapons, etc.) before routing.

## Gotchas
- Clear `__pycache__` after editing modules served by the running Flask app (stale .pyc caused 500s).
- `requirements.txt` deps (flask, numpy, scipy, matplotlib) installed to user site-packages; `rdkit`/`google.generativeai` optional (not installed) — modules degrade gracefully.
- Generated plots/schemes live in `static/plots/` and `static/reactions/` (gitignored).

## Git
Remote: origin → github.com/capizzinew-gif/zeno.git, branch: main.
