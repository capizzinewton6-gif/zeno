"""Knowledge engine: mathematical ontology and a small theorem graph.

Holds a curated set of well-known theorems/identities grouped by domain so that
agents can look up relevant facts. This is intentionally a small, verified
knowledge base; it is extended over time via the memory stores.
"""

from __future__ import annotations

from typing import Any

THEOREM_GRAPH: dict[str, list[dict[str, str]]] = {
    "algebra": [
        {"name": "Fundamental Theorem of Algebra",
         "statement": "Every non-constant polynomial with complex coefficients has at least one complex root.",
         "use": "Root-finding for polynomials over C."},
        {"name": "Lagrange's Theorem",
         "statement": "For a finite group G and subgroup H, |H| divides |G|.",
         "use": "Constraining subgroup orders."},
        {"name": "First Isomorphism Theorem",
         "statement": "G/ker(phi) ≅ im(phi) for a homomorphism phi: G -> H.",
         "use": "Quotient structure identification."},
    ],
    "analysis": [
        {"name": "Fundamental Theorem of Calculus",
         "statement": "If F' = f and f is continuous, then ∫_a^b f = F(b) - F(a).",
         "use": "Evaluating definite integrals via antiderivatives."},
        {"name": "Mean Value Theorem",
         "statement": "If f is continuous on [a,b] and differentiable on (a,b), ∃ c: f'(c)=(f(b)-f(a))/(b-a).",
         "use": "Bounding derivatives; proving inequalities."},
        {"name": "Cauchy-Schwarz Inequality",
         "statement": "|<u,v>| ≤ ||u|| ||v||.",
         "use": "Inner-product estimates."},
        {"name": "Taylor's Theorem",
         "statement": "f(x) = Σ f^(k)(a)/k! (x-a)^k + remainder.",
         "use": "Local series approximation."},
    ],
    "number_theory": [
        {"name": "Fundamental Theorem of Arithmetic",
         "statement": "Every integer >1 has a unique prime factorization (up to order).",
         "use": "Factorization; divisibility arguments."},
        {"name": "Fermat's Little Theorem",
         "statement": "a^p ≡ a (mod p) for prime p.",
         "use": "Modular exponentiation; primality hints."},
        {"name": "Chinese Remainder Theorem",
         "statement": "Coprime moduli yield a unique simultaneous solution mod their product.",
         "use": "Solving systems of congruences."},
        {"name": "Euler's Totient Theorem",
         "statement": "a^φ(n) ≡ 1 (mod n) when gcd(a,n)=1.",
         "use": "Reducing exponents modulo n."},
    ],
    "linear_algebra": [
        {"name": "Spectral Theorem",
         "statement": "A real symmetric matrix is orthogonally diagonalizable.",
         "use": "Eigen-decomposition; quadratic forms."},
        {"name": "Rank-Nullity Theorem",
         "statement": "rank(A) + nullity(A) = number of columns of A.",
         "use": "Dimension counting."},
    ],
    "combinatorics": [
        {"name": "Pigeonhole Principle",
         "statement": "If n items are placed in m<n boxes, some box has ≥2 items.",
         "use": "Existence counting arguments."},
        {"name": "Handshaking Lemma",
         "statement": "The sum of vertex degrees in a graph equals twice the edge count.",
         "use": "Parity arguments on graphs."},
    ],
    "probability": [
        {"name": "Law of Large Numbers",
         "statement": "Sample mean converges to the expected value as n→∞.",
         "use": "Monte Carlo convergence justification."},
        {"name": "Bayes' Theorem",
         "statement": "P(A|B)=P(B|A)P(A)/P(B).",
         "use": "Updating beliefs from evidence."},
    ],
}


class KnowledgeEngine:
    """Lookup interface over the theorem graph."""

    def __init__(self) -> None:
        self.graph = {k: list(v) for k, v in THEOREM_GRAPH.items()}

    def domains(self) -> list[str]:
        return list(self.graph)

    def lookup(self, domain: str) -> list[dict[str, str]]:
        return self.graph.get(domain, [])

    def search(self, query: str) -> list[dict[str, str]]:
        q = query.lower()
        out: list[dict[str, str]] = []
        for facts in self.graph.values():
            for fact in facts:
                if q in fact["name"].lower() or q in fact["statement"].lower():
                    out.append(fact)
        return out

    def verify_identity(self, lhs: Any, rhs: Any) -> bool:
        """Verify two symbolic expressions are equal using SymPy."""
        try:
            import sympy as sp
            diff = sp.simplify(sp.sympify(lhs) - sp.sympify(rhs))
            return diff == 0
        except Exception:
            return False
