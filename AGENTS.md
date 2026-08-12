# MATHEMATICS_AI — Project Memory

## Overview
Autonomous AI Mathematics Assistant & Research Environment. Python package `mathematics_ai` with 18 subsystems, 136 importable modules. One capability = one source code module.

## Run / Test
- Install: `pip install -e .` (dev mode). Console entry: `math-ai` (may need PATH); module form: `python -m mathematics_ai.main "<query>"`.
- Interactive REPL: `python -m mathematics_ai.main` (no args). UI in `mathematics_ai/ui.py`.
- One-shot: `python -m mathematics_ai.main "differentiate x^3"`.
- Batch: `python -m mathematics_ai.main --batch file.txt`.
- Tests: `python tests/test_full_system.py` and `python tests/test_subsystems.py` (both pure-stdlib asserts, no pytest needed). Both must print `ALL CHECKS PASSED`.
- Full import check: `python -c "import importlib,pkgutil,mathematics_ai; [importlib.import_module(m.name) for m in pkgutil.walk_packages(mathematics_ai.__path__,'mathematics_ai.')]"`.

## Architecture / Conventions
- Engines (mandated Gemini-only): `ai_core/gemini_25_flash_engine.py` (model_name="gemini-2.5-flash"), `ai_core/gemini_15_flash_engine.py` ("gemini-1.5-flash"), `ai_core/model_router.py`. All subclass `GeminiEngineBase` (`ai_core/engine_base.py`). Use `GEMINI_API_KEY` if present; otherwise deterministic local fallback (`engine.available == False`, router returns `[local-fallback] ...`). `EngineResponse` has `.text` (NOT `.content`).
- `src/` namespace mirrors spec: `src/{gemini_25_flash_engine,gemini_15_flash_engine,model_router}/__init__.py` are re-export shims of the engine/router CLASSES only (no `ENGINE_NAME`/`is_available` symbols exist).
- Leading-digit module names renamed to `dN_` prefix: `modeling/d1_structures.py`, `d2_manifolds.py`, `d3_geometry.py` (Python cannot import `1d_...`).
- `memory/` stores: `ListStore` (keyed list, `.all()`/`.add()`/`.items`) and `DictStore`. `research_notes` is a `ListStore` keyed on `"projects"`. NOTE: no `.load()`/`.save()` on stores — use `.all()` and `_data[key]`+`._save()`.
- `config.py` (module, not package) loads JSON from `config/` dir and exports `CONFIG_DIR`, `MEMORY_DIR`.
- `agents/base.py`: `BaseAgent` exposes `self.advanced` (2.5), `self.fast` (1.5), `self.router`; helper `self.result(answer, steps, success, **meta)` / `self.fail(error)`. `AgentResult` dataclass: `.answer/.steps/.metadata/.success/.error`.
- `agents/math_agent.py`: `MathAgent.solve(query)` classifies domain via `planning.detect_domain`, safety-checks, routes to handler. Sub-agents: `.compute .prover .conjecture .research .optimization .project`.
- `ProjectAgent` uses `memory.research_notes` store (fields `title`/`description`); `ResearchManager` uses `name`/`goal` — `list_projects` falls back `title or name`.
- `calculations/symbolic_math.py`: `_parse()` (tolerates `^` and implicit mult); `_parse_equation()` splits `lhs=rhs` into `sp.Eq` (plain `_parse` chokes on `=`). `solve()` uses `_parse_equation`.

## Key API facts (gotchas fixed during testing)
- `monte_carlo.monte_carlo_pi()` returns `{"estimate","error","samples"}` (key is `estimate`, not `pi`).
- `cellular_automata.evolve(rule, init, steps)` returns `steps+1` rows (includes initial).
- `dynamical_simulator.lyapunov_exponent_1d` returns `inf` for fully chaotic logistic map r=4.
- `error_bounds.Interval` has `.lo`/`.hi` (not `.lower`/`.a`).
- `numerical_computing/hpc_interface` has `eigvals/svd/lu_factor/solve/...` (no `detect_backend`).
- `premise_selection.retrieve(query)` matches by tag-keyword overlap; use "algebra"/"topology"/etc (not "induction").
- `topology_geometry`: `knot_theory_db.jones_polynomial_trefoil()`, `linking_number()`, `curvature_calculator.sphere_metric_ricci(r)`, `homology_engine.boundary_operator(simplices,dim)` then `betti_numbers([matrix])`, `lie_groups.get_cartan_matrix("A2")`/`root_system_A2()`, `space_classifier.classify_by_euler(dim,betti,closed)`.
- `modeling`: `domain_manager.Space(name,kind)` + `DomainManager.register()`; `d2_manifolds.surface_area_parametric()`/`graph_adjacency_matrix()`; `commutative_diagrams.Category().add_object(name).add_morphism(src,tgt,name)`; `vector_spaces.l2_inner_product/orthonormalize`; `axiom_rules.get_axioms("Peano")`.
- `vision/diagram_reader.parse_tikz_diagram` handles both `\\node name {label};` and `\\node (name) {label};` forms; edges via `\\draw (a) -- (b);`.

## Deps
sympy, numpy, scipy, mpmath, networkx, matplotlib, google-genai (lazy/optional). No OpenAI/Claude/etc.
