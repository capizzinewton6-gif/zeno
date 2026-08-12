"""End-to-end smoke test for the full Mathematics AI system.

Runs functional checks across every subsystem to confirm Phase 1 is runnable.
"""

from __future__ import annotations

import sys

import numpy as np

from mathematics_ai.agents.math_agent import MathAgent
from mathematics_ai.ui import MathematicsUI


def _check(label: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}{f' — {detail}' if detail else ''}")
    if not ok:
        _check.failed += 1
_check.failed = 0

def test_agent_end_to_end(agent: MathAgent) -> None:
    print("\n== MathAgent end-to-end ==")

    r = agent.solve("differentiate x^3")
    _check("differentiate x^3", r.success and "3*x**2" in str(r.answer), str(r.answer))

    r = agent.solve("integrate 2*x")
    _check("integrate 2*x", r.success and "x**2" in str(r.answer), str(r.answer))

    r = agent.solve("solve x^2 - 4 = 0")
    _check("solve x^2-4=0", r.success, str(r.answer))

    r = agent.solve("prove that sin(x)^2 + cos(x)^2 = 1")
    _check("prove pythagorean identity", r.success and r.answer is not None, str(r.answer))

    r = agent.solve("prove that 2 divides n^2+n for all n")
    _check("prove 2 | n^2+n", r.success, str(r.answer))

    seq = [1, 1, 2, 3, 5, 8]
    r = agent.conjecture.generate_from_sequence(seq, name="fib")
    _check("conjecture fibonacci", r.success, str(r.answer)[:80])

    r = agent.solve("minimize x^2+1 on [-2,2]")
    _check("optimize minimize", r.success, str(r.answer)[:80])

    r = agent.solve("oeis 1 1 2 3 5 8")
    _check("oeis lookup", r.success, str(r.answer)[:80])


def test_topology_geometry() -> None:
    print("\n== topology_geometry ==")
    import numpy as np
    from mathematics_ai.topology_geometry import (
        knot_theory_db, curvature_calculator, homology_engine, lie_groups, space_classifier,
    )
    j = knot_theory_db.jones_polynomial_trefoil()
    _check("knot jones trefoil", j is not None, str(j)[:60])

    ln = knot_theory_db.linking_number([(0, 1, 1), (1, 0, 1)])
    _check("linking number", ln == 1, str(ln))

    k = float(curvature_calculator.sphere_metric_ricci(2.0))
    _check("ricci scalar sphere", abs(k - 0.5) < 1e-9, str(k))

    b1 = homology_engine.boundary_operator([(0, 1), (1, 2), (0, 2)], 1)
    betti = homology_engine.betti_numbers([b1])
    _check("betti numbers triangle", isinstance(betti, list), str(betti))

    C = lie_groups.get_cartan_matrix("A2")
    _check("lie cartan A2", C == [[2, -1], [-1, 2]], str(C))

    roots = lie_groups.root_system_A2()
    _check("lie roots A2", len(roots) == 6, str(len(roots)))

    c = space_classifier.classify_by_euler(2, 2, True)
    _check("classify S2 by euler", "S2" in c, str(c))


def test_data_analysis() -> None:
    print("\n== data_analysis ==")
    from mathematics_ai.data_analysis import (
        statistical_engine, time_series_analysis, regression_models,
        anomaly_detection, data_summarizer,
    )
    s = statistical_engine.descriptive_stats([1, 2, 3, 4, 5])
    _check("descriptive stats", abs(s["mean"] - 3.0) < 1e-9, str(s))

    t = statistical_engine.t_test_one_sample([1.0, 2.0, 3.0, 4.0, 5.0], 3.0)
    _check("t-test", "p_value" in t, str(t))

    ar = time_series_analysis.ar_coefficients([1.0, 2.0, 3.0, 4.0, 5.0], p=1)
    _check("AR coefficients", len(ar) == 1, str(ar))

    lr = regression_models.linear_regression([1.0, 2.0, 3.0], [2.0, 4.0, 6.0])
    _check("linear regression", abs(lr["slope"] - 2.0) < 1e-6, str(lr))

    out = anomaly_detection.iqr_outliers([1.0, 1.0, 1.0, 1.0, 100.0])
    _check("iqr outlier", out == [4], str(out))

    m = data_summarizer.moments([1.0, 2.0, 3.0, 4.0, 5.0])
    _check("moments", "skewness" in m, str(m))


def test_vision() -> None:
    print("\n== vision ==")
    from mathematics_ai.vision import (
        equation_reader, diagram_reader, plot_digitizer,
        symbol_identifier, proof_image_analyzer, visual_topology_reader,
    )
    _check("equation reader (no key)", not equation_reader.extract_latex_from_image("x.png")["available"])

    parsed = diagram_reader.parse_tikz_diagram("\\node (a) {A}; \\draw (a) -- (b);")
    _check("tikz parse", len(parsed["nodes"]) >= 1, str(parsed))

    sym = symbol_identifier.name_to_symbol("alpha")
    _check("symbol alpha", sym == "α", str(sym))

    found = symbol_identifier.identify_from_text("use \\alpha and \\beta")
    _check("identify from text", len(found) == 2, str(found))

    struct = proof_image_analyzer.parse_proof_structure("Premise\nStep 1\nStep 2\nTherefore QED")
    _check("proof structure", len(struct["steps"]) == 2, str(struct))

    crossings = visual_topology_reader.count_crossings_from_projection(
        [(0, 0), (1, 1), (1, 0), (0, 1)], closed=False
    )
    _check("crossing count", crossings >= 1, str(crossings))


def test_visualization() -> None:
    print("\n== visualization ==")
    from mathematics_ai.visualization import (
        manifold_renderer, graph_plotter, vector_field_plotter,
        complex_domain_plotter, geometric_construction, proof_tree_visualizer,
    )
    torus = manifold_renderer.render_torus(resolution=5)
    _check("render torus", "x" in torus and len(torus["x"]) == 5, "ok")

    layout = graph_plotter.spring_layout([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    _check("spring layout", len(layout) == 3, str(layout))

    topo = graph_plotter.topological_sort([[0, 1, 0], [0, 0, 1], [0, 0, 0]])
    _check("topo sort", topo == [0, 1, 2], str(topo))

    field = vector_field_plotter.direction_field(lambda x, y: 1.0, lambda x, y: -1.0, resolution=4)
    _check("direction field", "u" in field, "ok")

    dc = complex_domain_plotter.domain_coloring(lambda z: z ** 2, resolution=5)
    _check("domain coloring", "image" in dc, "ok")

    tri = geometric_construction.construct_equilateral_triangle(1.0)
    _check("equilateral triangle", len(tri) == 3, str(tri))

    tree = proof_tree_visualizer.build_proof_tree([
        {"id": 1, "statement": "A", "rule": "axiom", "depends_on": []},
        {"id": 2, "statement": "B", "rule": "modus", "depends_on": [1]},
    ])
    _check("proof tree", len(tree["edges"]) == 1, str(tree))
    _check("ascii tree", "1" in proof_tree_visualizer.to_ascii_tree(tree))


def test_database() -> None:
    print("\n== database ==")
    from mathematics_ai.database import (
        theorems_lemmas_db, oeis_sequences_db, formulas_identities_db,
        formal_libraries_db, algebraic_structures_db,
    )
    _check("theorem search", len(theorems_lemmas_db.search("arithmetic")) >= 1)
    _check("theorem get", theorems_lemmas_db.get("Pythagorean Theorem") is not None)

    _check("oeis by id", oeis_sequences_db.get_by_id("A000108") is not None)
    matches = oeis_sequences_db.search_by_prefix([0, 1, 1, 2, 3, 5])
    _check("oeis prefix", any(m["oeis_id"] == "A000045" for m in matches), str(matches))

    _check("formula search", len(formulas_identities_db.search("euler")) >= 1)
    _check("formal libs", len(formal_libraries_db.by_system("Lean 4")) >= 1)
    _check("alg structures", algebraic_structures_db.get("Z_2") is not None)


def test_project() -> None:
    print("\n== project ==")
    from mathematics_ai.project import (
        research_manager, task_manager, notebook_manager, documentation, paper_generator,
    )
    tm = task_manager.TaskManager()
    tm.add("Prove lemma X", "lemma")
    tm.complete(0)
    _check("task manager", tm.summary()["done"] == 1, str(tm.summary()))

    rm = research_manager.ResearchManager()
    proj = rm.create("Test Project", "test conjectures")
    _check("research manager create", proj.name == "Test Project", proj.id)
    rm.add_note(proj.id, "initial observation")
    _check("research manager note", len(rm.get(proj.id).notes) == 1)

    doc = documentation.generate_document("Test", [{"heading": "Intro", "content": "Hello"}])
    _check("latex doc", "\\section{Intro}" in doc)

    paper = paper_generator.generate_paper(
        "My Paper", ["Author"], "Abstract", [{"heading": "Intro", "content": "Body"}],
        theorems=[{"name": "theorem", "statement": "1=1", "proof": "trivial"}],
    )
    _check("paper generator", "\\begin{abstract}" in paper and "\\begin{theorem}" in paper)


def test_ui(agent: MathAgent) -> None:
    print("\n== UI ==")
    ui = MathematicsUI(agent=agent)
    _check("UI constructed", ui.agent is agent)

    # dispatch a domain command without running the REPL
    ui.dispatch("differentiate x^3")


def main() -> int:
    agent = MathAgent()
    test_agent_end_to_end(agent)
    test_topology_geometry()
    test_data_analysis()
    test_vision()
    test_visualization()
    test_database()
    test_project()
    test_ui(agent)
    print("\n" + "=" * 60)
    if _check.failed:
        print(f"FAILED: {_check.failed} check(s) failed")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
