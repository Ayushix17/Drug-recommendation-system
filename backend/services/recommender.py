from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

from backend.graph.knowledge_graph import Drug, load_knowledge_graph
from backend.services.alternatives import check_hard_conflicts, safe_alternatives
from backend.services.risk_scoring import compute_risk_score


def normalize_tags(values: List[str]) -> Set[str]:
    return {value.strip().lower().replace(" ", "_") for value in values if value and value.strip()}


@dataclass
class AcceptedRecommendation:
    drug: str
    risk_score: int
    reasons: List[str]
    alternatives_considered: List[str]


@dataclass
class RejectedRecommendation:
    drug: str
    reasons: List[str]
    alternatives: List[str]


class RecommenderService:
    def __init__(self, data_dir: str | Path = "data") -> None:
        self.graph, self.drugs, self.disease_to_drugs, self.interactions = load_knowledge_graph(data_dir)

    def diseases(self) -> List[str]:
        return sorted(self.disease_to_drugs.keys())

    def graph_summary(self) -> Dict[str, int]:
        edge_count = sum(len(items) for items in self.graph.edges.values())
        return {"nodes": len(self.graph.nodes), "edges": edge_count}

    def recommend(
        self,
        disease: str,
        age: int,
        allergies: List[str],
        history: List[str],
        current_medications: List[str],
    ) -> Dict[str, object]:
        disease_key = disease.strip().lower().replace(" ", "_")
        if disease_key not in self.disease_to_drugs:
            return {
                "error": f"Disease '{disease}' not found",
                "available_diseases": self.diseases(),
            }

        allergy_set = normalize_tags(allergies)
        history_set = normalize_tags(history)
        meds_set = normalize_tags(current_medications)

        accepted: List[AcceptedRecommendation] = []
        rejected: List[RejectedRecommendation] = []

        for drug_name in sorted(self.disease_to_drugs[disease_key]):
            drug: Drug = self.drugs[drug_name]
            conflicts = check_hard_conflicts(allergy_set, history_set, drug)
            if conflicts:
                rejected.append(
                    RejectedRecommendation(
                        drug=drug_name,
                        reasons=conflicts,
                        alternatives=safe_alternatives(allergy_set, history_set, drug, self.drugs),
                    )
                )
                continue

            risk_score, reasons = compute_risk_score(
                age=age,
                history=history_set,
                current_medications=meds_set,
                candidate_drug=drug,
                interactions=self.interactions,
            )
            accepted.append(
                AcceptedRecommendation(
                    drug=drug_name,
                    risk_score=risk_score,
                    reasons=reasons,
                    alternatives_considered=sorted(drug.alternatives),
                )
            )

        accepted.sort(key=lambda item: item.risk_score)
        return {
            "disease": disease_key,
            "accepted": [item.__dict__ for item in accepted],
            "rejected": [item.__dict__ for item in rejected],
            "graph_summary": self.graph_summary(),
        }
