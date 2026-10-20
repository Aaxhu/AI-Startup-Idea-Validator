import pytest
from agents.competitor_researcher import CompetitorResearchAgent

def test_generate_queries_restaurant():
    agent = CompetitorResearchAgent()
    idea = "An AI platform for small restaurants that predicts daily food demand and inventory"
    analysis = {
        "industry": "Food Service",
        "startup_category": "Food Technology",
        "target_audience": "Small Restaurants",
        "customer_pain_point": "Food Waste, Inventory",
        "value_proposition": "Demand Forecasting, Inventory Management"
    }
    queries = agent.generate_queries(idea, analysis)
    assert len(queries) >= 3
    # Check that queries do NOT contain 'startup idea validator'
    for q in queries:
        assert "startup idea validator" not in q.lower()
    # At least one query mentions food or restaurant
    combined = " ".join(queries).lower()
    assert "food" in combined or "restaurant" in combined

def test_generate_queries_student_validator():
    agent = CompetitorResearchAgent()
    idea = "An AI platform that helps students discover and validate startup ideas"
    analysis = {
        "industry": "Education Technology",
        "startup_category": "Education Technology",
        "target_audience": "Students",
        "customer_pain_point": "Idea Validation",
        "value_proposition": "Startup Idea Validation"
    }
    queries = agent.generate_queries(idea, analysis)
    assert len(queries) >= 3
    combined = " ".join(queries).lower()
    assert "student" in combined or "education" in combined or "startup" in combined
