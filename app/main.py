import sys

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from pipeline.run import run_pipeline


app = FastAPI(
    title="AI Startup Idea Validator",
    description="Backend API for AI-powered startup idea validation",
    version="1.0.0",
)


class StartupIdeaRequest(BaseModel):
    startup_idea: str = Field(
        ...,
        min_length=10,
        description="Startup idea to validate",
    )


@app.get("/")
def root():
    return {
        "message": "AI Startup Idea Validator API is running",
        "status": "online",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.post("/validate")
def validate_startup_idea(request: StartupIdeaRequest):

    try:
        result = run_pipeline(request.startup_idea)

        return {
            "status": "success",
            "startup_idea": result["startup_idea"],
            "idea_analysis": result["idea_analysis"].model_dump(),
            "market_research": result["market_research"].model_dump(),
            "competitor_research": result["competitor_research"].model_dump(),
            "swot_analysis": result["swot_analysis"].model_dump(),
            "strategy": result["strategy"].model_dump(),
            "final_recommendation": result[
                "final_recommendation"
            ].model_dump(),
            "report": result["report"],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Startup validation failed: {str(e)}",
        )