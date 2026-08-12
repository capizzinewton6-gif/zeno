"""Math agent: the main mathematical intelligence orchestrator.

Single entry point that accepts a high-level mathematical request, classifies
it, and delegates to the appropriate specialized agent (compute, prover,
conjecture, research, optimization). Coordinates multi-step workflows.
"""

from __future__ import annotations

import re
from typing import Any

from mathematics_ai.agents.base import BaseAgent, AgentResult
from mathematics_ai.agents.compute_agent import ComputeAgent
from mathematics_ai.agents.prover_agent import ProverAgent
from mathematics_ai.agents.conjecture_agent import ConjectureAgent
from mathematics_ai.agents.research_agent import ResearchAgent
from mathematics_ai.agents.optimization_agent import OptimizationAgent
from mathematics_ai.agents.project_agent import ProjectAgent
from mathematics_ai.ai_core import ReasoningEngine, ContextManager, KnowledgeEngine, SafetyLayer, PlanningEngine


class MathAgent(BaseAgent):
    """Top-level mathematical assistant."""

    name = "math_agent"

    def __init__(self) -> None:
        super().__init__()
        self.compute = ComputeAgent()
        self.prover = ProverAgent()
        self.conjecture = ConjectureAgent()
        self.research = ResearchAgent()
        self.optimization = OptimizationAgent()
        self.project = ProjectAgent()
        self.context = ContextManager()
        self.knowledge = KnowledgeEngine()
        self.safety = SafetyLayer()
        self.planning = PlanningEngine()
        self.reasoning = ReasoningEngine(self.advanced)

    # --- dispatch ----------------------------------------------------
    def solve(self, query: str) -> AgentResult:
        """Classify and route a natural-language mathematical query."""
        self.context.push(query)
        domain = self.planning.detect_domain(query)
        steps = [{"domain": domain}]
        if self.context.current is not None:
            self.context.current.record("classification", f"detected domain: {domain}")

        # 1. Safety / resource check
        safety = self.safety.check_provable(query)
        steps.append({"safety": safety})
        if safety["provable"] == "unprovable":
            return self.result(
                {"answer": f"This statement appears to be unprovable: {safety['note']}", "domain": domain},
                steps=steps,
                handled_by="safety_layer",
            )

        # 2. Route to the right handler
        handler = self._route(query, domain)
        steps.append({"handler": handler.__name__})
        return handler(query, domain, steps)

    # --- handlers ----------------------------------------------------
    def _route(self, query: str, domain: str):
        q = query.lower()
        if any(k in q for k in ("prove", "verify", "show that", "is divisible by", "disprove", "identity")):
            return self._handle_proof
        if any(k in q for k in ("oeis", "arxiv", "look up", "search", "find paper", "research")):
            return self._handle_research
        if any(k in q for k in ("minimize", "maximize", "optim", "linear program", "least squares", "fit")):
            return self._handle_optimization
        if any(k in q for k in ("conjecture", "pattern", "predict next", "sequence")):
            return self._handle_conjecture
        return self._handle_compute

    def _handle_compute(self, query: str, domain: str, steps: list[dict[str, Any]]) -> AgentResult:
        op, args = self._parse_compute_query(query)
        if op is None:
            # fallback: just return a textual analysis via reasoning engine
            trace = self.reasoning.reason_about(query, context="compute fallback")
            steps.append({"reasoning": trace.as_dict()})
            last = trace.steps[-1].statement if trace.steps else "no steps"
            return self.result(
                {"answer": f"Analyzed query in domain '{domain}': {last}",
                 "trace": trace.as_dict()},
                steps=steps,
                handled_by="reasoning",
            )
        res = self.compute.compute(op, **args)
        res.steps = steps + res.steps
        res.metadata["domain"] = domain
        res.metadata["handled_by"] = "compute_agent"
        return res

    def _handle_proof(self, query: str, domain: str, steps: list[dict[str, Any]]) -> AgentResult:
        res = self.prover.prove(query)
        res.steps = steps + res.steps
        res.metadata["domain"] = domain
        res.metadata["handled_by"] = "prover_agent"
        return res

    def _handle_conjecture(self, query: str, domain: str, steps: list[dict[str, Any]]) -> AgentResult:
        seq = _extract_sequence(query)
        if seq:
            res = self.conjecture.generate_from_sequence(seq, name="user_query")
        else:
            res = self.conjecture.test_conjecture(query, lambda n: True)
        res.steps = steps + res.steps
        res.metadata["domain"] = domain
        res.metadata["handled_by"] = "conjecture_agent"
        return res

    def _handle_optimization(self, query: str, domain: str, steps: list[dict[str, Any]]) -> AgentResult:
        # minimal parser: "minimize x^2+1 on [-2,2]"
        m = re.search(r"minimize\s+(.+?)\s+on\s+\[(-?\d+\.?\d*),\s*(-?\d+\.?\d*)\]", query, re.IGNORECASE)
        if m:
            expr, a, b = m.group(1), float(m.group(2)), float(m.group(3))
            import sympy as sp
            f = sp.lambdify("x", sp.sympify(expr), "numpy")
            res = self.optimization.constrained(f, [(a, b)], [(a + b) / 2])
        else:
            res = self.optimization.minimize(lambda x: sum(v ** 2 for v in x), [1.0, 1.0])
        res.steps = steps + res.steps
        res.metadata["domain"] = domain
        res.metadata["handled_by"] = "optimization_agent"
        return res

    def _handle_research(self, query: str, domain: str, steps: list[dict[str, Any]]) -> AgentResult:
        seq = _extract_sequence(query)
        topic = re.sub(r"(search|find|look up|research)\s*", "", query, flags=re.IGNORECASE).strip() or domain
        res = self.research.research(topic, sequence=seq)
        res.steps = steps + res.steps
        res.metadata["domain"] = domain
        res.metadata["handled_by"] = "research_agent"
        return res

    # --- query parser ------------------------------------------------
    def _parse_compute_query(self, query: str) -> tuple[str | None, dict[str, Any]]:
        q = query.lower().strip()

        # "differentiate x^3" / "derivative of x^3"
        m = re.match(r"(?:differentiate|derivative of)\s+(.+?)(?:\s+w\.?r\.?t\.?\s+(\w+))?$", q)
        if m:
            return "differentiate", {"expr": m.group(1), "var": m.group(2) or "x"}

        m = re.match(r"integrate\s+(.+?)(?:\s+d(\w))?(?:\s+from\s+(-?\d+\.?\d*)\s+to\s+(-?\d+\.?\d*))?$", q)
        if m:
            args = {"expr": m.group(1), "var": m.group(2) or "x"}
            if m.group(3) is not None:
                args["a"], args["b"] = m.group(3), m.group(4)
            return "integrate", args

        m = re.match(r"limit\s+of\s+(.+?)\s+as\s+(\w+)\s*->\s*(-?\d+\.?\d*)", q)
        if m:
            return "limit", {"expr": m.group(1), "var": m.group(2), "to": m.group(3)}

        m = re.match(r"solve\s+(.+?)(?:\s+for\s+(\w+))?$", q)
        if m:
            return "solve", {"expr": m.group(1), "var": m.group(2) or "x"}

        m = re.match(r"simplify\s+(.+)$", q)
        if m:
            return "simplify", {"expr": m.group(1)}

        # number theory - integer factorization (must precede polynomial factor)
        m = re.match(r"factor(?:ize)?\s+(\d+)$", q)
        if m:
            return "factorize", {"n": int(m.group(1))}
        m = re.match(r"factor(?:ize)?\s+(.+?)(?:\s+for\s+(\w+))?$", q)
        if m:
            return "factor", {"expr": m.group(1), "var": m.group(2) or "x"}

        m = re.match(r"taylor(?:\s+series)?\s+(?:of\s+)?(.+?)(?:\s+around\s+(-?\d+\.?\d*))?(?:\s+order\s+(\d+))?$", q)
        if m:
            args = {"expr": m.group(1), "around": m.group(2) or 0, "n": int(m.group(3) or 6)}
            return "series", args

        # number theory
        m = re.match(r"is\s+(\d+)\s+prime", q)
        if m:
            return "is_prime", {"n": int(m.group(1))}
        m = re.match(r"factor(?:ize)?\s+(\d+)$", q)
        if m:
            return "factorize", {"n": int(m.group(1))}
        m = re.match(r"totient\s+of\s+(\d+)", q)
        if m:
            return "totient", {"n": int(m.group(1))}
        m = re.match(r"(?:binomial|choose)\s+(\d+)\s+(\d+)", q)
        if m:
            return "binomial", {"n": int(m.group(1)), "k": int(m.group(2))}
        m = re.match(r"catalan\s+(\d+)", q)
        if m:
            return "catalan", {"n": int(m.group(1))}
        m = re.match(r"partitions?\s+of\s+(\d+)", q)
        if m:
            return "partitions", {"n": int(m.group(1))}

        # linear algebra
        m = re.search(r"eigenvalues?\s+of\s+(.+)", q)
        if m:
            mat = _parse_matrix(m.group(1))
            if mat:
                return "eigenvalues", {"matrix": mat}
        m = re.search(r"determinant\s+of\s+(.+)", q)
        if m:
            mat = _parse_matrix(m.group(1))
            if mat:
                return "determinant", {"matrix": mat}

        return None, {}


def _extract_sequence(query: str) -> list[int] | None:
    m = re.search(r"\[(-?\d+(?:\s*,\s*-?\d+)+)\]", query)
    if m:
        return [int(x.strip()) for x in m.group(1).split(",")]
    m = re.search(r"sequence\s+(?:of\s+)?(-?\d+(?:\s*,\s*-?\d+)+)", query)
    if m:
        return [int(x.strip()) for x in m.group(1).split(",")]
    return None


def _parse_matrix(s: str) -> list[list[float]] | None:
    """Parse a matrix given like [[1,2],[3,4]] or 1,2;3,4."""
    import ast
    s = s.strip().rstrip(".")
    try:
        v = ast.literal_eval(s)
        if isinstance(v, list) and v and isinstance(v[0], list):
            return v
    except Exception:
        pass
    # try semicolon rows
    try:
        rows = [r for r in s.replace("[", "").replace("]", "").split(";") if r.strip()]
        mat = [[float(x) for x in row.split(",")] for row in rows]
        if mat:
            return mat
    except Exception:
        return None
    return None
