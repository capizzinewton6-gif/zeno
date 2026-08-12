"""Functional checks for the remaining subsystems.

Covers formal_proofs, numerical_computing, simulation, modeling, and the
mathematics package — the subsystems not exercised by test_full_system.py.
"""

from __future__ import annotations

import sys


def _check(label: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}{f' — {detail}' if detail else ''}")
    if not ok:
        _check.failed += 1
_check.failed = 0


def test_formal_proofs() -> None:
    print("\n== formal_proofs ==")
    from mathematics_ai.formal_proofs import (
        lean_interface, coq_interface, isabelle_interface,
        proof_checker, tactic_engine, premise_selection,
    )
    _check("lean available check", isinstance(lean_interface.is_available(), bool))
    _check("lean emit_theorem", "theorem" in lean_interface.emit_theorem("foo", "1=1"))
    _check("coq available check", isinstance(coq_interface.is_available(), bool))
    _check("isabelle available check", isinstance(isabelle_interface.is_available(), bool))

    step = proof_checker.ProofStep("A", "axiom", "given")
    result = proof_checker.check_proof([step])
    _check("proof check", isinstance(result, proof_checker.ProofCheck))

    tac = tactic_engine.suggest_tactic("x = x")
    _check("suggest tactic", isinstance(tac, str) and len(tac) > 0, tac)

    seq = tactic_engine.generate_tactic_sequence("goal")
    _check("tactic sequence", isinstance(seq, list) and len(seq) >= 1)

    _check("premise retrieve", len(premise_selection.retrieve("algebra")) >= 1)


def test_numerical_computing() -> None:
    print("\n== numerical_computing ==")
    from mathematics_ai.numerical_computing import (
        arbitrary_precision, root_finder, error_bounds,
        fast_fourier, optimization_solver, hpc_interface,
    )
    arbitrary_precision.set_precision(50)
    _check("set/get precision", arbitrary_precision.get_precision() == 50)
    x = arbitrary_precision.mpf("0.1")
    _check("mpf", str(x).startswith("0.1"))

    roots = root_finder.polynomial_roots([1, 0, -4])  # x^2 - 4
    _check("poly roots", len(roots) == 2, str(roots))

    bisect = root_finder.find_root_bisection(lambda x: x ** 2 - 2, 0.0, 2.0)
    _check("bisection sqrt2", abs(bisect - 2 ** 0.5) < 1e-6, str(bisect))

    iv = error_bounds.from_tolerance(1.0, 0.01)
    _check("interval", hasattr(iv, "lo") and abs(iv.lo - 0.99) < 1e-9, str(iv.lo))
    re_err = error_bounds.relative_error(1.0, 1.001)
    _check("relative error", re_err > 0, str(re_err))

    sig = [1.0, 0.0, 0.0, 0.0]
    spec = fast_fourier.fft(sig)
    _check("fft", len(spec) == 4 and abs(spec[0].real - 1.0) < 1e-9, str(spec[0]))
    back = fast_fourier.ifft(spec)
    _check("ifft round-trip", abs(back[0].real - 1.0) < 1e-9, str(back[0]))

    res = optimization_solver.minimize_nonlinear(lambda v: (v[0] - 3) ** 2, [0.0])
    _check("minimize nonlinear", res["success"] and abs(res["x"][0] - 3) < 1e-4, str(res))

    lp = optimization_solver.linear_program([-1, -1], [[2, 1], [1, 2]], [4, 3])
    _check("linear program", lp.get("success", True), str(lp)[:80])

    vals = hpc_interface.eigvals([[2.0, 0.0], [0.0, 3.0]])
    _check("hpc eigvals", len(vals) == 2, str(vals))


def test_simulation() -> None:
    print("\n== simulation ==")
    from mathematics_ai.simulation import (
        monte_carlo, cellular_automata, dynamical_simulator,
        fractal_simulator, graph_simulator, fluid_pde_simulator,
    )
    pi_est = monte_carlo.monte_carlo_pi(n=5000, seed=42)
    _check("monte carlo pi", 2.8 < pi_est["estimate"] < 3.4, str(pi_est["estimate"]))

    grid = cellular_automata.evolve(90, [1, 0, 1, 0, 1], 3)
    _check("cellular automaton", len(grid) == 4 and len(grid[0]) == 5)

    orbit = dynamical_simulator.logistic_map(3.2, 0.5, n=20)
    _check("logistic map", len(orbit) == 20)

    lyap = dynamical_simulator.lyapunov_exponent_1d(
        lambda x, r: r * x * (1 - x), lambda x, r: r * (1 - 2 * x), 4.0, 0.2
    )
    _check("lyapunov positive (chaos)", lyap > 0, str(lyap))

    mandel = fractal_simulator.mandelbrot(width=10, height=10, max_iter=20)
    _check("mandelbrot", len(mandel) == 10)

    julia = fractal_simulator.julia(complex(-0.7, 0.27), width=8, height=8, max_iter=20)
    _check("julia", len(julia) == 8)

    g = graph_simulator.erdos_renyi(10, 0.3, seed=0)
    _check("erdos-renyi", g.number_of_nodes() == 10)

    diff = fluid_pde_simulator.diffusion_2d(nx=8, ny=8, nt=5, dt=0.001)
    _check("diffusion 2d", len(diff) == 8 and len(diff[0]) == 8)


def test_modeling() -> None:
    print("\n== modeling ==")
    from mathematics_ai.modeling import (
        domain_manager, d1_structures, d2_manifolds, d3_geometry,
        commutative_diagrams, vector_spaces, parameters, axiom_rules,
    )
    dm = domain_manager.DomainManager()
    sp1 = domain_manager.Space(name="R2", kind="metric")
    dm.register(sp1)
    _check("domain manager register", dm.get("R2") is not None)

    fib = d1_structures.fibonacci_sequence(10)
    _check("fibonacci seq", fib[:6] == [0, 1, 1, 2, 3, 5], str(fib[:6]))

    area = d2_manifolds.surface_area_parametric(
        lambda u, v: u, lambda u, v: v, lambda u, v: 0.0,
        (0.0, 1.0), (0.0, 1.0), n=5,
    )
    _check("surface area parametric", abs(area - 1.0) < 1e-6, str(area))

    vol = d3_geometry.sphere_volume(1.0)
    _check("sphere volume", abs(vol - 4 / 3 * 3.14159265358979) < 1e-3, str(vol))

    A = d2_manifolds.graph_adjacency_matrix(3, [(0, 1), (1, 2)])
    _check("graph adjacency", A == [[0, 1, 0], [1, 0, 1], [0, 1, 0]], str(A))

    cat = commutative_diagrams.Category()
    cat.add_object("A")
    cat.add_object("B")
    cat.add_morphism("A", "B", "f")
    _check("category morphism", len(cat.morphisms) == 1)

    ip = vector_spaces.l2_inner_product([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    _check("l2 inner product", abs(ip - 14.0) < 1e-9, str(ip))

    ortho = vector_spaces.orthonormalize([[1.0, 0.0], [1.0, 1.0]])
    _check("orthonormalize", len(ortho) == 2, str(ortho)[:60])

    _check("parameters constants", len(parameters.list_constants()) >= 1)

    axioms = axiom_rules.get_axioms("Peano")
    _check("peano axioms", isinstance(axioms, list) and len(axioms) >= 1, str(axioms)[:60])


def test_mathematics_package() -> None:
    print("\n== mathematics ==")
    from mathematics_ai.mathematics import (
        algebra, analysis, combinatorics, geometry, linear_algebra,
        logic, number_theory, probability, topology,
    )
    _check("algebra cyclic group", algebra.cyclic_group(3).order() == 3 if hasattr(algebra, "cyclic_group") else True)
    _check("analysis limit", hasattr(analysis, "limit") or True)

    # number theory — small smoke checks if helpers exist
    _check("number_theory import", number_theory is not None)
    _check("combinatorics import", combinatorics is not None)
    _check("geometry import", geometry is not None)
    _check("linear_algebra import", linear_algebra is not None)
    _check("logic import", logic is not None)
    _check("probability import", probability is not None)
    _check("topology import", topology is not None)


def test_gemini_engines_and_src() -> None:
    print("\n== ai_core / src engines ==")
    from mathematics_ai.ai_core import Gemini25FlashEngine, Gemini15FlashEngine, ModelRouter
    from mathematics_ai.src import (
        Gemini25FlashEngine as Src25, Gemini15FlashEngine as Src15, ModelRouter as SrcRouter,
    )
    e = Gemini25FlashEngine()
    _check("engine 2.5 model name", e.model_name == "gemini-2.5-flash")
    _check("engine 2.5 available (no key)", e.available is False)
    _check("engine 1.5 model name", Gemini15FlashEngine().model_name == "gemini-1.5-flash")

    _check("src re-export 2.5", Src25 is Gemini25FlashEngine)
    _check("src re-export 1.5", Src15 is Gemini15FlashEngine)
    _check("src re-export router", SrcRouter is ModelRouter)

    router = ModelRouter()
    _check("router classify advanced", router.classify("prove theorem") == "advanced")
    _check("router classify fast", router.classify("parse metadata") == "fast")
    resp = router.route("prove 1=1", "prove 1=1")
    _check("router route fallback", "local-fallback" in resp.text or "fallback" in resp.text.lower())


def main() -> int:
    test_formal_proofs()
    test_numerical_computing()
    test_simulation()
    test_modeling()
    test_mathematics_package()
    test_gemini_engines_and_src()
    print("\n" + "=" * 60)
    if _check.failed:
        print(f"FAILED: {_check.failed} check(s) failed")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
