from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple


def _split_pipe(value: str) -> Set[str]:
    if not value:
        return set()
    return {token.strip().lower().replace(" ", "_") for token in value.split("|") if token.strip()}


@dataclass(frozen=True)
class Drug:
    name: str
    indications: Set[str]
    contraindications: Set[str]
    allergy_tags: Set[str]
    side_effect_severity: int
    alternatives: Set[str]


@dataclass
class KnowledgeGraph:
    nodes: Set[str] = field(default_factory=set)
    edges: Dict[str, List[Tuple[str, str]]] = field(default_factory=dict)

    def add_node(self, node: str) -> None:
        self.nodes.add(node)
        self.edges.setdefault(node, [])

    def add_edge(self, source: str, relation: str, target: str) -> None:
        self.add_node(source)
        self.add_node(target)
        self.edges[source].append((relation, target))


def load_knowledge_graph(data_dir: str | Path = "data") -> tuple[
    KnowledgeGraph, Dict[str, Drug], Dict[str, Set[str]], Dict[frozenset, int]
]:
    base = Path(data_dir)
    drugs_file = base / "drugs.csv"
    diseases_file = base / "diseases.csv"
    interactions_file = base / "interactions.csv"

    drugs: Dict[str, Drug] = {}
    with drugs_file.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row["name"].strip().lower()
            drugs[name] = Drug(
                name=name,
                indications=_split_pipe(row["indications"]),
                contraindications=_split_pipe(row["contraindications"]),
                allergy_tags=_split_pipe(row["allergy_tags"]),
                side_effect_severity=int(row["side_effect_severity"]),
                alternatives=_split_pipe(row["alternatives"]),
            )

    disease_to_drugs: Dict[str, Set[str]] = {}
    with diseases_file.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            disease = row["disease"].strip().lower().replace(" ", "_")
            disease_to_drugs[disease] = _split_pipe(row["drugs"])

    interactions: Dict[frozenset, int] = {}
    with interactions_file.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pair = frozenset({row["drug_a"].strip().lower(), row["drug_b"].strip().lower()})
            interactions[pair] = int(row["risk"])

    graph = KnowledgeGraph()
    for disease, disease_drugs in disease_to_drugs.items():
        for drug_name in disease_drugs:
            graph.add_edge(f"disease:{disease}", "treated_by", f"drug:{drug_name}")
    for drug_name, drug in drugs.items():
        for condition in drug.contraindications:
            graph.add_edge(f"drug:{drug_name}", "contraindicated_for", f"condition:{condition}")
        for alternative in drug.alternatives:
            graph.add_edge(f"drug:{drug_name}", "alternative_to", f"drug:{alternative}")
    for pair, risk in interactions.items():
        first, second = sorted(pair)
        graph.add_edge(f"drug:{first}", f"interacts_with:risk_{risk}", f"drug:{second}")
        graph.add_edge(f"drug:{second}", f"interacts_with:risk_{risk}", f"drug:{first}")

    return graph, drugs, disease_to_drugs, interactions
