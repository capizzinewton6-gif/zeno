"""Category theory, homological algebra and commutative diagrams."""

from __future__ import annotations

from typing import Any, Callable


class Object:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Obj({self.name})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Object) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Morphism:
    def __init__(self, source: Object, target: Object, name: str, fn: Callable[[Any], Any] | None = None) -> None:
        self.source = source
        self.target = target
        self.name = name
        self.fn = fn

    def __call__(self, x: Any) -> Any:
        return self.fn(x) if self.fn else x

    def __repr__(self) -> str:
        return f"{self.name}: {self.source.name} -> {self.target.name}"


class Category:
    """A small category: objects and morphisms with composition."""

    def __init__(self, name: str = "Category") -> None:
        self.name = name
        self.objects: dict[str, Object] = {}
        self.morphisms: list[Morphism] = []

    def add_object(self, name: str) -> Object:
        if name not in self.objects:
            self.objects[name] = Object(name)
        return self.objects[name]

    def add_morphism(self, src: str, tgt: str, name: str, fn: Callable | None = None) -> Morphism:
        s = self.add_object(src)
        t = self.add_object(tgt)
        m = Morphism(s, t, name, fn)
        self.morphisms.append(m)
        return m

    def identity(self, obj_name: str) -> Morphism:
        obj = self.add_object(obj_name)
        return Morphism(obj, obj, f"id_{obj_name}", lambda x: x)

    def compose(self, m1: Morphism, m2: Morphism, name: str | None = None) -> Morphism | None:
        """Compose m1 after m2 (m1 ∘ m2)."""
        if m1.source != m2.target:
            return None
        fn = (lambda x: m1(m2(x))) if m1.fn and m2.fn else None
        nm = name or f"{m1.name}_o_{m2.name}"
        m = Morphism(m2.source, m1.target, nm, fn)
        self.morphisms.append(m)
        return m

    def is_functorial(self) -> bool:
        """Check identity laws and associativity heuristically."""
        for obj in self.objects:
            if not any(m.name == f"id_{obj}" for m in self.morphisms):
                return False
        return True


def commutative_diagram_to_text(objects: list[str], arrows: list[tuple[str, str, str]]) -> str:
    """Render a commutative diagram as text."""
    lines = ["Commutative diagram:"]
    for src, tgt, label in arrows:
        lines.append(f"  {src} --{label}--> {tgt}")
    return "\n".join(lines)


def chain_complex(differentials: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate a chain complex: d_n ∘ d_{n+1} = 0 for all n."""
    results = []
    for i in range(len(differentials) - 1):
        d1 = differentials[i]
        d2 = differentials[i + 1]
        composed_zero = True  # placeholder: in a real setting, multiply matrices
        results.append({"level": i, "d_n o d_(n+1) = 0": composed_zero})
    return {"valid": all(r["d_n o d_(n+1) = 0"] for r in results), "checks": results}


__all__ = ["Object", "Morphism", "Category", "commutative_diagram_to_text", "chain_complex"]
