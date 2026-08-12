"""Generate pathway maps and genetic circuit diagrams."""
from __future__ import annotations


class DiagramGenerator:
    @staticmethod
    def pathway_diagram(nodes: list[str], edges: list[tuple[str, str]],
                        title: str = "Pathway Map") -> str:
        """Generate a Mermaid flowchart of a metabolic pathway."""
        lines = [f"```mermaid", f"flowchart LR",
                 f"  %% {title}"]
        for a, b in edges:
            lines.append(f"  {a} --> {b}")
        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def genetic_circuit_diagram(promoter: str, rbs: str, cds: str,
                                terminator: str) -> str:
        """SBOL-style inline text diagram of a genetic circuit."""
        return (f"[{promoter}] --(transcription)--> [{rbs}] "
                f"--(translation)--> [{cds}] --(stop)--> [{terminator}]")

    @staticmethod
    def plasmid_map(features: list[dict]) -> str:
        """Text-based circular plasmid map summary."""
        lines = ["Plasmid Map (linearized):"]
        for f in sorted(features, key=lambda x: x.get("start", 0)):
            lines.append(
                f"  {f.get('start', '?')}-{f.get('end', '?')} bp: "
                f"{f.get('name', 'feature')} ({f.get('type', 'misc')})"
            )
        return "\n".join(lines)

    @staticmethod
    def cladogram(tree: dict, indent: int = 0) -> str:
        """Render a nested dict tree as an indented text cladogram."""
        lines = []
        for name, children in tree.items():
            lines.append("  " * indent + f"- {name}")
            if isinstance(children, dict):
                lines.append(DiagramGenerator.cladogram(children, indent + 1))
        return "\n".join(lines)
