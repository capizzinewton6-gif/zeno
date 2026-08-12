"""Knowledge engine: graph connecting identities, objects, and relationships."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class Entity:
    id: str
    kind: str  # person | object | location | event
    attributes: Dict[str, object] = field(default_factory=dict)
    relations: List[str] = field(default_factory=list)


class KnowledgeEngine:
    """An in-memory knowledge graph linking identities, objects, and locations."""

    def __init__(self) -> None:
        self.entities: Dict[str, Entity] = {}

    def add_entity(self, entity: Entity) -> None:
        self.entities[entity.id] = entity

    def get(self, entity_id: str) -> Entity:
        if entity_id not in self.entities:
            raise KeyError(f"Unknown entity '{entity_id}'")
        return self.entities[entity_id]

    def link(self, source_id: str, target_id: str, relation: str = "related") -> None:
        if source_id in self.entities:
            self.entities[source_id].relations.append(f"{relation}:{target_id}")

    def query(self, kind: str = "", text: str = "") -> List[Entity]:
        result = []
        for e in self.entities.values():
            if kind and e.kind != kind:
                continue
            if text and text.lower() not in str(e.attributes).lower():
                continue
            result.append(e)
        return result

    def related(self, entity_id: str) -> List[Entity]:
        e = self.entities.get(entity_id)
        if not e:
            return []
        out: List[Entity] = []
        for rel in e.relations:
            target = rel.split(":", 1)[1]
            if target in self.entities:
                out.append(self.entities[target])
        return out

    def all_ids(self) -> Set[str]:
        return set(self.entities.keys())
