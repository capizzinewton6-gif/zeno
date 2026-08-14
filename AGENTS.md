# zeno - Autonomous Computer AI Assistant

## Overview
Capability-based autonomous computer AI assistant (a.k.a. "Paperclip"). Gemini
2.5 Flash is the reasoning engine; Gemini 1.5 Flash is the processing engine.
A deterministic offline fallback keeps the system fully runnable without an API
key.

## Architecture
- `main.py` - entry point (interactive REPL or `--task` single-shot). `--no-daemons` skips background loops.
- `smart_orchestrator.py` - central brain; plans via `Orchestrator`, routes to capabilities, summarizes.
- `orchestrator.py` - LLM planner; emits JSON step arrays `[{step, capability, args}]`.
- `core/capability.py` - `Capability` base class (`execute`/`get_name`/`get_description` + `ok`/`error`/`result_to_text` helpers).
- `core/llm.py` - `LLMClient`: wraps `google-generativeai` when `GEMINI_API_KEY`/`GOOGLE_API_KEY` set; deterministic local planner/summarizer fallback otherwise.
- `ai_models/llm_gemini.py` - Gemini wrapper delegating to `core.llm.LLMClient`.
- `integrations/ai_model_router.py` - the router the orchestrator uses; exposes `reason`/`process`/`summarize`.
- `actions/` (~245), `automation/`, `smart_agents/`, `sensors/`, `autonomy/`, `security/`, `integrations/`, `ai_models/` - capability packages, each with `__init__.py` auto-discovery (`get_modules()`/`get_actions()`).

## Capability contract
Every module exposes `execute(task, context=None)` + `get_name()` + `get_description()`.
Modules inherit `core.capability.Capability`. Result dicts use `{"status":"ok","result":...}`
or `{"status":"error","error":...}`.

## Implemented (real) actions
`terminal_manager`, `file_controller`, `system_monitor`, `web_search`,
`url_launcher`, `ip_checker`, `qr_generator`, `reminder`, `note_taker`,
`weather_report`, `translation_service`, `app_manager`, `screenshot`,
`music_player`, `calendar_manager`, `gmail_sender`, `calculator`.
All other modules remain stubs (`{"status":"stub"}`).

## Run
```bash
pip install psutil requests rich loguru pyyaml
python main.py --no-daemons                          # interactive
python main.py --task "calculate 12 * (3 + 4)" --no-daemons
python main.py --task "system status" --no-daemons
GEMINI_API_KEY=... python main.py                    # real Gemini planning
```

## Test
```bash
python tests/test_core.py        # 19 hermetic tests (no network)
```

## Key conventions
- Offline fallback is the default (no key in this env). Routing is keyword-based (`CAPABILITY_KEYWORDS` in `smart_orchestrator.py`).
- `build_structure.py` is the scaffolding generator; module template uses `.format()` so braces are escaped as `{{`/`}}`.
- Tasks often arrive as the full objective string in `step["args"]`; action modules must strip their own command prefixes (e.g. "calculate", "generate qr").
- Never enable destructive commands without confirmation (`TerminalManager.dangerous` blocklist).
