from models.schemas import Strategy
from tools.llm import llm_client


class StrategyAgent:

    def run(
        self,
        startup_idea: str,
        idea_analysis: dict,
        market_research: dict,
        competitor_research: dict,
        swot_analysis: dict,
    ) -> Strategy:

        system_prompt = """
You are a startup strategy and MVP planning expert.

Create a practical startup strategy using the provided
idea, market research, competitor research, and SWOT analysis.

Return ONLY valid JSON.
No Markdown.
No explanations outside JSON.

Keep all text concise and practical.
Do not invent exact financial numbers.
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

SWOT ANALYSIS:
{swot_analysis}

Create a realistic MVP and business strategy.

Return ONLY this JSON:

{{
  "mvp_plan": [
    {{
      "feature": "feature name",
      "priority": "Must Have",
      "rationale": "why this feature is needed"
    }},
    {{
      "feature": "feature name",
      "priority": "Should Have",
      "rationale": "why this feature is useful"
    }},
    {{
      "feature": "feature name",
      "priority": "Could Have",
      "rationale": "why this feature can be added later"
    }}
  ],
  "mvp_timeline_weeks": 8,
  "revenue_streams": [
    {{
      "stream": "revenue source",
      "model": "pricing model",
      "estimated_arpu": "estimate required"
    }},
    {{
      "stream": "revenue source",
      "model": "pricing model",
      "estimated_arpu": "estimate required"
    }}
  ],
  "pricing_strategy": "short pricing strategy",
  "go_to_market_strategy": "short GTM strategy",
  "customer_acquisition_channels": [
    "channel 1",
    "channel 2",
    "channel 3"
  ],
  "growth_plan": "short growth plan",
  "burn_rate_estimate": "Estimate required",
  "key_milestones": [
    "milestone 1",
    "milestone 2",
    "milestone 3"
  ],
  "summary": "short strategy summary"
}}

Rules:

- Maximum 5 MVP features.
- Use realistic priorities: Must Have, Should Have, Could Have.
- MVP timeline must be between 4 and 16 weeks.
- Maximum 3 customer acquisition channels.
- Maximum 4 milestones.
- Do not invent exact revenue or burn-rate figures.
- Focus on students as the initial target audience.
"""

        return llm_client.generate_structured(
            system_prompt,
            user_prompt,
            Strategy,
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

    swot_analysis = {
        "strengths": [
            "AI-powered personalized recommendations",
            "Efficient startup idea validation",
            "Growing interest in AI tools",
        ],
        "weaknesses": [
            "Dependence on accurate data",
            "Limited initial market research",
            "Competition from existing platforms",
        ],
        "opportunities": [
            "Growing AI education market",
            "Student entrepreneurship",
            "Educational institution partnerships",
        ],
        "threats": [
            "Established competitors",
            "Inaccurate recommendations",
            "Changing AI technology",
        ],
        "overall_viability": "High",
        "key_risk": (
            "Dependence on accurate data for recommendations"
        ),
        "summary": (
            "The startup has strong potential but requires "
            "reliable data and clear differentiation."
        ),
    }

    agent = StrategyAgent()

    result = agent.run(
        startup_idea,
        idea_analysis,
        market_research,
        competitor_research,
        swot_analysis,
    )

    print("\n===== STRATEGY & MVP =====")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()