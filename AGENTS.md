# Zeno - Autonomous AI Inventor

## Project Memory

### Build Status
COMPLETED:
- Task 1-3: Foundation, AI Core, Engineering modules
- Task 4: ALL invention packages complete (design, calculations, simulation,
  electronics, robotics, prototyping, materials, vision, manufacturing,
  research, project, tools)
- Task 5: Autonomous agents package (7 agents)
- Task 6: Automation modules (src/painter_automation, src/notepad_automation,
  src/invention_workflow_engine)
- Task 7: Text-based UI (ui.py) + main.py entry point
- Task 8: memory/ package (MemoryStore)

### Architecture
- One Capability = One Module
- Gemini 2.5 Flash (primary, deep reasoning) + Gemini 1.5 Flash (secondary, fast)
- Engineering modules take KnowledgeEngine; all others take Gemini25FlashEngine
- Engines degrade to deterministic offline stub without GEMINI_API_KEY
- Painter/Notepad drive Windows apps via pyautogui, fall back to direct files

### Verified
- All 22 packages import cleanly
- All 7 agents instantiate and respond
- End-to-end workflow: 17 blueprints + 17 docs + BOM + summary + ZIP
- UI loop and one-shot CLI commands work
- Tools: Calculator, FormulaEngine, DataAnalyzer, GraphGenerator, FileManager

### Run
```
python main.py                    # interactive UI
python main.py invent "..."       # one-shot invention workflow
python main.py engineer "..."     # one-shot engineering solve
```
Set GEMINI_API_KEY for live model responses.
