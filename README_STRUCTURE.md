# Autonomous Computer AI Assistant

Capability-based source code architecture. One capability = one source code module.

## Top-level files

| File | Role |
|------|------|
| `main.py` | Entry point; starts AI + all daemons |
| `ui.py` | Text-based Python UI |
| `setup.py` | Installs dependencies, sets up permissions and runtime dirs |
| `orchestrator.py` | LLM planner that breaks tasks into steps |
| `smart_orchestrator.py` | Central brain that routes to everything |

## Packages

| Package | Modules | Purpose |
|---------|--------|---------|
| `actions/` | 245 | Individual tools (system, files, web, media, comms, finance, legal, IoT, ...) |
| `automation/` | 27 | Workflow modules |
| `smart_agents/` | 20 | High-level role-based agents |
| `sensors/` | 12 | Perception modules |
| `autonomy/` | 12 | Decision modules |
| `security/` | 12 | Safety modules |
| `integrations/` | 15 | Connection modules |
| `ai_models/` | 10 | AI model wrappers |
| `memory/` | 8 | Data stores |
| `core/` | 1 | System prompt |
| `config/` | 1 | API keys |

**Total modules: 353**

## AI engine

Powered exclusively by Google Gemini models:
- **Gemini 2.5 Flash** - reasoning, planning, autonomous decisions
- **Gemini 1.5 Flash** - fast processing, extraction, summarisation

The `integrations/ai_model_router.py` can also route to Claude / GPT / Llama.

## Quick start

```bash
python setup.py            # install deps + create runtime dirs/secrets
# edit config/api_keys.json with your keys
python main.py             # interactive mode
python main.py --task "Search the web for today's top AI news"
```

## Architecture

Every module in `actions/`, `automation/`, `smart_agents/`, `sensors/`,
`autonomy/`, `security/`, `integrations/` and `ai_models/` is fully
independent and exposes the standard `execute(task, context)` contract.
Each package `__init__.py` auto-registers its modules, so the smart
orchestrator discovers capabilities at runtime without manual imports.

## License

MIT License
