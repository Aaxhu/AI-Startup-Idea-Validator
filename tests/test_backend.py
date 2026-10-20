import pytest
from fastapi.testclient import TestClient
from app.main import app
from models.schemas import (
    IdeaAnalysis,
    MarketResearch,
    MarketTrend,
    Competitor,
    CompetitorResearch,
    SWOTAnalysis,
    MVPFeature,
    RevenueStream,
    Strategy,
    FinalRecommendation,
)

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_validate_request_validation():
    # Less than min_length=10 should return 422
    response = client.post("/validate", json={"startup_idea": "short"})
    assert response.status_code == 422


def test_schemas():
    idea = IdeaAnalysis(
        industry="Food Tech",
        target_audience="Small restaurants",
        customer_pain_point="Food waste and unpredictable demand",
        value_proposition="AI food demand forecasting",
        startup_category="SaaS",
        key_assumptions=["Historical sales predict demand"],
        feasibility_score=8,
        summary="A platform for predicting food demand.",
    )
    assert idea.feasibility_score == 8

    swot = SWOTAnalysis(
        strengths=["AI accuracy"],
        weaknesses=["Requires initial data"],
        opportunities=["Large restaurant market"],
        threats=["Competition"],
        overall_viability="High",
        key_risk="Data integration friction",
        summary="Solid market potential.",
    )
    assert swot.overall_viability == "High"

    rec = FinalRecommendation(
        verdict="GO WITH CHANGES",
        confidence=8,
        rationale="Strong market pull",
        top_3_priorities=["Integrate POS", "Test with 5 restaurants", "Build MVP"],
        biggest_risk="Data integration friction",
    )
    assert rec.verdict == "GO WITH CHANGES"
