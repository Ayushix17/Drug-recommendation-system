from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.routes.recommend import router as recommend_router

app = FastAPI(
    title="Personalized Drug Recommendation Engine",
    version="1.0.0",
    description="Medication recommendation API using patient profile, disease mapping, interaction checks, and risk scoring.",
)
app.include_router(recommend_router)


@app.get("/")
def root() -> JSONResponse:
    return JSONResponse(
        {
            "name": "Personalized Drug Recommendation Engine API",
            "status": "ok",
            "docs": "/docs",
            "health": "/health",
            "endpoints": ["/diseases", "/graph/summary", "/recommend"],
            "note": "This Vercel deployment serves the FastAPI backend.",
        }
    )
