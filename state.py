from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel

from models.schemas import (
    IdeaAnalysis,
    MarketResearch,
    CompetitorResearch,
    SWOTAnalysis,
    Strategy,
    FinalRecommendation,
)


class AgentState(BaseModel):
    """Shared state passed through every agent in the pipeline."""

    run_id: str = str(uuid4())

    created_at: str = datetime.now(timezone.utc).isoformat()

    startup_idea: str

    idea_analysis: Optional[IdeaAnalysis] = None

    market_research: Optional[MarketResearch] = None

    competitor_research: Optional[CompetitorResearch] = None

    swot_analysis: Optional[SWOTAnalysis] = None

    strategy: Optional[Strategy] = None

    final_recommendation: Optional[FinalRecommendation] = None

    report_path: Optional[str] = None

    status: str = "pending"

    error: Optional[str] = None

    def mark_running(self) -> None:
        self.status = "running"
        self.error = None

    def mark_completed(self) -> None:
        self.status = "completed"

    def mark_failed(self, error: str) -> None:
        self.status = "failed"
        self.error = error

    def to_dict(self) -> dict:
        return self.model_dump(mode="json")