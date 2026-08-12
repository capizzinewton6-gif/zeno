# Zeno - Autonomous AI Vision & Scene Understanding Assistant

## Overview
A text-GUI-based AI Vision and Scene Understanding Assistant. Uses Google Gemini
2.5 Flash (reasoning) and Gemini 1.5 Flash (fast vision) exclusively. Architecture:
**one capability = one source code module**.

## Architecture
Top-level entry points:
- `main.py` - CLI entry point (`python main.py --stream 0` / `--image path.jpg`)
- `ui.py` - Text GUI driving `VisionAgent` over live/synthetic streams

Packages:
- `agents/` - orchestration: `vision_agent` (top) + object_detector, face_recognizer,
  tracking, research, optimization, project sub-agents
- `ai_core/` - AI decision intelligence: `ai_engine`, reasoning, planning, context,
  knowledge, safety_layer, `prompt.txt`
- `src/gemini_25_flash_engine/` and `src/gemini_15_flash_engine/` - Gemini wrappers
- `modeling/` + `calculations/` - shared kernel (math + data structures)
- `core_vision/` - camera, preprocess, detection, recognition, features, spatial, flow, postproc
- `facial_processing/` - aligner, embeddings, matcher, gallery, anti-spoof, attributes, identity
- `tracking_analytics/` - tracker, trajectory, persistence, occlusion, interactions, heatmap, events
- `vision_input/` - ocr, scene, gesture, barcode/qr, quality, apparatus
- `edge_computing/` - cuda, tensorrt, openvino, stream_pipeline, memory, device_manager
- `visualization/` - overlay, landmarks, tracking_viz, dashboard, alerts, video_writer
- `simulation/` - synthetic_stream, occlusion, stress_tester, tracking_eval, latency_profiler, benchmark
- `security_compliance/` - encryption, anonymizer, access_control, audit_logger, privacy_scrubber
- `research/`, `project/`, `tools/` - supporting utilities
- `memory/*.json`, `config/*.json`, `database/*.db` - data stores

## Key Technical Decisions
- **Digit-prefixed modules**: `2d_boxes.py` and `3d_cuboids.py` can't be imported
  directly via `from modeling.2d_boxes import ...`. Created re-export shims
  `two_d_boxes.py` / `three_d_cuboids.py` that register the real module in `sys.modules`
  and re-export its symbols. Always import via the `two_d_boxes`/`three_d_cuboids` names.
- **Offline-first Gemini**: all engines degrade gracefully when `GEMINI_API_KEY`
  is absent. `fast_analyze` returns an error dict; `extract_text` returns "" (empty)
  on offline/error so downstream consumers get clean strings.
- **Optional deps**: OpenCV, torch/ultralytics, dlib, faiss, cryptography, google-genai
  are all optional. Missing deps fall back to numpy-only implementations.
- **Audit logger**: the hash chain uses `prev_hash` + fields EXCEPT `hash` in the
  payload for `verify()` to match `log()`. Do not include the `hash` field when
  recomputing.
- **JPEG encode**: use `cv2.IMWRITE_JPEG_QUALITY` (=1) not a literal int 101.

## Running
```bash
python main.py                       # synthetic stream, text GUI
python main.py --stream 0            # local webcam
python main.py --image path.jpg      # single image, exit
python tests/test_integration.py     # 11 integration tests (all pass offline)
```

## Test Status (as of build completion)
- 11/11 integration tests pass
- 0 failed imports across all 126 .py files in all packages
- Verified end-to-end: VisionAgent.perceive() + analyze_static() on synthetic frames

## Conventions
- Every module has `from __future__ import annotations`
- Dataclasses for all result/config types
- `try/except ImportError` guards for optional heavy deps (cv2, torch, etc.)
- One capability = one source file; package `__init__.py` re-exports public classes
