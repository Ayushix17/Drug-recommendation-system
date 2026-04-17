from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.models.schemas import RecommendationRequest, RecommendationResponse
from backend.services.recommender import RecommenderService

router = APIRouter()
service = RecommenderService(data_dir="data")


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/diseases")
def diseases() -> dict[str, list[str]]:
    return {"diseases": service.diseases()}


@router.get("/graph/summary")
def graph_summary() -> dict[str, int]:
    return service.graph_summary()


@router.post("/recommend", response_model=RecommendationResponse)
def recommend(payload: RecommendationRequest) -> RecommendationResponse:
    result = service.recommend(
        disease=payload.disease,
        age=payload.age,
        allergies=payload.allergies,
        history=payload.history,
        current_medications=payload.current_medications,
    )
    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail={
                "error": result["error"],
                "available_diseases": result["available_diseases"],
            },
        )
    return RecommendationResponse(**result)
