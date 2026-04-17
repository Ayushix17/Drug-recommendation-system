from __future__ import annotations

from typing import Dict, List, Set, Tuple

from backend.graph.knowledge_graph import Drug


def check_hard_conflicts(allergies: Set[str], history: Set[str], drug: Drug) -> List[str]:
    reasons: List[str] = []
    if allergies & drug.allergy_tags:
        reasons.append(
            f"allergy conflict: patient allergies {sorted(allergies)} match {sorted(drug.allergy_tags)}"
        )

    contraindications = history & drug.contraindications
    if contraindications:
        reasons.append(f"contraindicated due to history {sorted(contraindications)}")

    return reasons


def safe_alternatives(
    allergies: Set[str],
    history: Set[str],
    drug: Drug,
    all_drugs: Dict[str, Drug],
) -> List[str]:
    options: List[str] = []
    for alternative in sorted(drug.alternatives):
        alt_drug = all_drugs.get(alternative)
        if not alt_drug:
            continue
        if check_hard_conflicts(allergies, history, alt_drug):
            continue
        options.append(alternative)
    return options
