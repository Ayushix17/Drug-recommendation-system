from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    disease: str = Field(..., description="Disease/condition, e.g. hypertension")
    age: int = Field(..., ge=0, le=130)
    allergies: List[str] = Field(default_factory=list)
    history: List[str] = Field(default_factory=list)
    current_medications: List[str] = Field(default_factory=list)


class AcceptedRecommendation(BaseModel):
    drug: str
    risk_score: int
    reasons: List[str]
    alternatives_considered: List[str]


class RejectedRecommendation(BaseModel):
    drug: str
    reasons: List[str]
    alternatives: List[str]


class RecommendationResponse(BaseModel):
    disease: str
    accepted: List[AcceptedRecommendation]
    rejected: List[RejectedRecommendation]
    graph_summary: dict[str, int]
