# Zeno - Screen Recognition AI

## Overview
A Gemini-powered screen recognition and automation AI. The system is built so that
**one capability = one source code module**, following a strict package structure
(see `ai_core/prompt.txt` and the project tree).

## AI Engine
Powered exclusively by Google Gemini models, configured in `config/model_config.json`:
- **Gemini 2.5 Flash** — Primary Engineering Intelligence Engine (reasoning, planning,
  security analysis, autonomous decision making, workflow orchestration). Used by
  `AIEngine.reason()` and `ReasoningModel`.
- **Gemini 1.5 Flash** — High-Speed Processing & Analysis Engine (fast context
  processing, OCR, metadata extraction, lightweight reasoning). Used by
  `AIEngine.analyze_fast()`.

Set `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) to enable live AI. Without it the engine
runs in a deterministic offline stub mode so all modules remain importable and testable.

## Architecture (top-level)
- `main.py` — application controller + CLI entry point (`python main.py`, `--command`,
  `--analyze`, `--gui`).
- `ui.py` — REPL + optional Tkinter GUI.
- `agents/` — orchestrators: `screen_agent` (top-level), `visual_agent`,
  `assistant_agent`, `automation_agent`, `learning_agent`.
- `ai_core/` — `ai_engine` (Gemini wrapper), `reasoning_engine`, `context_manager`,
  `command_parser`, `prompt.txt`.
- `ai_models/` — `vision_model`, `ocr_model`, `object_model`, `ui_model`,
  `reasoning_model` (each wraps a Gemini capability).
- `screen_capture/` — `screen_recorder`, `screenshot_manager`, `multi_monitor`,
  `frame_stream`, `capture_optimizer` (use `mss`).
- `recognition/` — UI elements, OCR, windows, icons, cursor, objects, layout.
- `computer_vision/` — image stats, patterns, colors, change/motion detection,
  visual memory (use `opencv`, `numpy`, `Pillow`).
- `understanding/` — screen/app/webpage/document/game/error interpretation.
- `automation/` — mouse/keyboard controllers, click/typing automation, workflow
  builder, task executor (use `pyautogui`).
- `integrations/` — OS abstraction, browser/app control, external HTTP tools.
- `security/` — `permission_manager` (action gating), `privacy_control` (redaction),
  `encryption` (Fernet with base64 fallback).
- `memory/` — JSON memory: screen_history, application_memory, ui_patterns,
  user_preferences.
- `database/` — SQLite: screenshots.db, applications.db, actions.db,
  recognition_logs.db.
- `config/` — settings.json, model_config.json, screen_config.json.

## Run / Test
```
pip install -r requirements.txt        # optional heavy deps
python main.py                          # REPL
python main.py --command "describe screen"
python main.py --analyze
python main.py --gui
```
All modules import cleanly even when optional deps (mss, pyautogui, opencv,
google-generativeai, cryptography, pytesseract) are absent — each falls back to a
no-op or stub. Set `GEMINI_API_KEY` to enable live Gemini reasoning.

## Conventions
- Optional third-party imports are wrapped in try/except with graceful fallbacks.
- Every Gemini call goes through `AIEngine`; reasoning = 2.5 Flash, fast = 1.5 Flash.
- Permission gating (`security/permission_manager`) guards destructive automation.
- Privacy redaction (`security/privacy_control`) protects sensitive screen text.
