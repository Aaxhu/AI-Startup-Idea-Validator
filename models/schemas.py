from typing import List, Optional, Any
from pydantic import BaseModel, Field, model_validator


class IdeaAnalysis(BaseModel):
    industry: str
    target_audience: str
    customer_pain_point: str
    value_proposition: str
    startup_category: str
    key_assumptions: List[str] = Field(default_factory=list)
    feasibility_score: int = Field(ge=1, le=10)
    summary: str


class MarketTrend(BaseModel):
    trend: str
    impact: str
    detail: str


class MarketResearch(BaseModel):
    total_addressable_market: str
    serviceable_addressable_market: str
    serviceable_obtainable_market: str
    market_growth_rate: str
    key_trends: List[MarketTrend] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    market_maturity: str
    summary: str


class Competitor(BaseModel):
    name: str
    website: Optional[str] = None
    description: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    funding_stage: Optional[str] = None
    approximate_users_or_revenue: Optional[str] = None


class CompetitorResearch(BaseModel):
    direct_competitors: List[Competitor] = Field(default_factory=list)
    indirect_competitors: List[Competitor] = Field(default_factory=list)
    market_gaps: List[str] = Field(default_factory=list)
    competitive_intensity: str
    differentiation_opportunities: List[str] = Field(default_factory=list)
    summary: str


class SWOTAnalysis(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    overall_viability: str
    key_risk: str
    summary: str


class MVPFeature(BaseModel):
    feature: str
    priority: str
    rationale: str


class RevenueStream(BaseModel):
    stream: str = ""
    model: str = ""
    estimated_arpu: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def normalise_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("stream"):
                for alias in (
                    "feature",
                    "name",
                    "type",
                    "title",
                    "revenue_stream",
                ):
                    if data.get(alias):
                        data["stream"] = data[alias]
                        break

            if not data.get("model"):
                for alias in (
                    "pricing_model",
                    "revenue_model",
                    "type",
                    "kind",
                ):
                    if data.get(alias):
                        data["model"] = data[alias]
                        break

        return data


class Strategy(BaseModel):
    mvp_plan: List[MVPFeature] = Field(default_factory=list)
    mvp_timeline_weeks: int
    revenue_streams: List[RevenueStream] = Field(default_factory=list)
    pricing_strategy: str
    go_to_market_strategy: str
    customer_acquisition_channels: List[str] = Field(default_factory=list)
    growth_plan: str
    burn_rate_estimate: Optional[str] = None
    key_milestones: List[str] = Field(default_factory=list)
    summary: str


class FinalRecommendation(BaseModel):
    verdict: str
    confidence: int = Field(ge=1, le=10)
    rationale: str
    top_3_priorities: List[str]
    biggest_risk: str