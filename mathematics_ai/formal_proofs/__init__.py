"""Formal proof interfaces (Lean/Coq/Isabelle) and tactic engine."""
from mathematics_ai.formal_proofs import (
    lean_interface, coq_interface, isabelle_interface,
    proof_checker, tactic_engine, premise_selection,
)
__all__ = ["lean_interface", "coq_interface", "isabelle_interface", "proof_checker", "tactic_engine", "premise_selection"]
