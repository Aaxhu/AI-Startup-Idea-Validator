from models.schemas import SWOTAnalysis
from tools.llm import llm_client


class SWOTRiskAgent:

    def run(
        self,
        startup_idea: str,
        idea_analysis: dict,
        market_research: dict,
        competitor_research: dict,
    ) -> SWOTAnalysis:

        system_prompt = """
You are a startup SWOT and risk analyst.

Analyze the startup using the provided idea,
market research, and competitor research.

Return ONLY valid JSON.
Do not use Markdown.
Do not invent exact statistics.
Keep every point short, specific, and practical.
"""

        user_prompt = f"""
STARTUP IDEA:
{startup_idea}

IDEA ANALYSIS:
{idea_analysis}

MARKET RESEARCH:
{market_research}

COMPETITOR RESEARCH:
{competitor_research}

Return ONLY this JSON structure:

{{
  "strengths": [
    "specific strength",
    "specific strength",
    "specific strength"
  ],
  "weaknesses": [
    "specific weakness",
    "specific weakness",
    "specific weakness"
  ],
  "opportunities": [
    "specific opportunity",
    "specific opportunity",
    "specific opportunity"
  ],
  "threats": [
    "specific threat",
    "specific threat",
    "specific threat"
  ],
  "overall_viability": "High/Medium/Low",
  "key_risk": "single biggest risk",
  "summary": "short overall SWOT summary"
}}

Rules:
- Maximum 3 items in each SWOT category.
- Base the analysis on the supplied information.
- Do not invent competitors.
- Do not invent exact market numbers.
- Focus on practical startup risks.
"""

        return llm_client.generate_structured(
            system_prompt,
            user_prompt,
            SWOTAnalysis,
        )


def main():

    startup_idea = (
        "An AI platform that helps students discover "
        "and validate startup ideas."
    )

    idea_analysis = {
        "industry": "Education Technology",
        "target_audience": "Students",
        "customer_pain_point": (
            "Difficulty in finding and validating startup ideas"
        ),
        "value_proposition": (
            "AI-powered platform to help students discover "
            "and validate startup ideas"
        ),
        "startup_category": "Education Technology",
    }

    market_research = {
        "total_addressable_market": "Estimate required",
        "serviceable_addressable_market": "Estimate required",
        "serviceable_obtainable_market": "Estimate required",
        "market_growth_rate": "Estimate required",
        "key_trends": [],
        "opportunities": [
            "Growing interest in AI tools",
            "Increasing student entrepreneurship"
        ],
        "market_maturity": "Growing",
        "summary": (
            "AI-powered education and startup tools "
            "are an emerging market."
        ),
    }

    competitor_research = {
        "direct_competitors": [
            {"name": "IdeaProof"},
            {"name": "Preuve"},
            {"name": "Aistartupvalidator"},
            {"name": "Feedough"},
            {"name": "Ideascan"},
        ],
        "indirect_competitors": [
            {"name": "FounderUplift"},
            {"name": "StartupDeck"},
            {"name": "StartupCheck"},
            {"name": "Ideanexus"},
            {"name": "ValidatorAI"},
        ],
        "market_gaps": [
            "Limited market research",
            "Limited competitor analysis",
            "Limited personalized recommendations",
        ],
        "competitive_intensity": "Low",
        "differentiation_opportunities": [
            "AI-powered idea validation",
            "Market research",
            "Personalized recommendations",
        ],
        "summary": (
            "Several startup idea validation platforms "
            "already exist."
        ),
    }

    agent = SWOTRiskAgent()

    result = agent.run(
        startup_idea,
        idea_analysis,
        market_research,
        competitor_research,
    )

    print("\n===== SWOT & RISK ANALYSIS =====")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()