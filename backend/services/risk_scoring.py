from __future__ import annotations

from typing import Dict, List, Set

from backend.graph.knowledge_graph import Drug


def compute_risk_score(
    age: int,
    history: Set[str],
    current_medications: Set[str],
    candidate_drug: Drug,
    interactions: Dict[frozenset, int],
) -> tuple[int, List[str]]:
    score = candidate_drug.side_effect_severity
    reasons: List[str] = [f"base side-effect severity +{candidate_drug.side_effect_severity}"]

    if age >= 65:
        score += 1
        reasons.append("age >= 65 sensitivity +1")
    elif age <= 12:
        score += 1
        reasons.append("pediatric caution +1")

    for medication in sorted(current_medications):
        interaction_risk = interactions.get(frozenset({candidate_drug.name, medication}))
        if interaction_risk:
            score += interaction_risk
            reasons.append(f"interaction with {medication} +{interaction_risk}")

    caution_overlap = history & {"kidney_disease", "liver_disease", "asthma"}
    if caution_overlap:
        score += 1
        reasons.append(f"comorbidity caution for {sorted(caution_overlap)} +1")

    return score, reasons
