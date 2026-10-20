from models.schemas import FinalRecommendation
from tools.llm import llm_client


class FinalRecommendationAgent:

    def run(
        self,
        startup_idea: str,
        idea_analysis: dict,
        market_research: dict,
        competitor_research: dict,
        swot_analysis: dict,
        strategy: dict,
    ) -> FinalRecommendation:

        system_prompt = """
You are a startup investment and validation advisor.

Evaluate the complete startup analysis and provide a balanced
final recommendation.

Return ONLY valid JSON.
Do not use Markdown.
Do not add explanations outside JSON.

Do not invent facts, companies, statistics, market data,
risks, priorities, or recommendations.

Use only the information provided in the analysis.

IMPORTANT:
The SWOT analysis is the primary source for identifying
the biggest risk.

The "key_risk" field from the SWOT analysis must be preserved
as the "biggest_risk" in the final recommendation unless there
is a clear contradiction in the supplied evidence.

Do not replace the SWOT key risk with a new risk such as
funding, investment, regulation, mobile development,
technology changes, or other risks unless that risk is explicitly
supported by the supplied analysis.
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

STRATEGY:
{strategy}

Based on all the above information, provide the final startup
recommendation.

IMPORTANT CONSISTENCY RULE:

The SWOT ANALYSIS contains a field called "key_risk".

The value of:

SWOT key_risk = {swot_analysis.get("key_risk", "")}

must be used as the final recommendation's:

biggest_risk

Do NOT create a different biggest risk.

The final recommendation must remain consistent with
the SWOT analysis.

Return ONLY JSON in this exact structure:

{{
    "verdict": "GO WITH CHANGES",
    "confidence": 7,
    "rationale": "A concise evidence-based explanation",
    "top_3_priorities": [
        "A specific actionable priority based on the analysis",
        "A second specific actionable priority based on the analysis",
        "A third specific actionable priority based on the analysis"
    ],
    "biggest_risk": "The same key risk identified by the SWOT analysis"
}}

Rules:

1. verdict must be exactly one of:
   "GO"
   "GO WITH CHANGES"
   "NO-GO"

2. confidence must be an integer from 1 to 10.

3. top_3_priorities must contain exactly 3 REAL,
   specific and actionable priorities.

4. Never write:
   "priority 1"
   "priority 2"
   "priority 3"

5. Priorities must be based on the actual startup analysis.

6. biggest_risk MUST exactly match the SWOT analysis key_risk.

7. Do not invent market statistics.

8. Do not introduce new risks that are not present
   in the supplied analysis.

9. Return JSON only.
"""

        return llm_client.generate_structured(
            system_prompt,
            user_prompt,
            FinalRecommendation,
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
        "summary": (
            "Growing opportunity for AI-powered education "
            "and startup validation tools."
        )
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
        "competitive_intensity": "Low",
        "market_gaps": [
            "Limited market research capabilities",
            "Insufficient competitor analysis",
            "Limited go-to-market strategy support",
        ],
    }

    swot_analysis = {
        "overall_viability": "High",
        "key_risk": (
            "Dependence on accurate data for recommendations"
        ),
        "summary": (
            "Strong potential with competition and "
            "data-quality risks."
        ),
    }

    strategy = {
        "mvp_timeline_weeks": 12,
        "pricing_strategy": "Freemium",
        "go_to_market_strategy": "Influencer Marketing",
        "customer_acquisition_channels": [
            "Social Media",
            "Online Communities",
            "Influencer Partnerships",
        ],
        "summary": (
            "Focus on students, AI-powered idea validation, "
            "and market research."
        ),
    }

    agent = FinalRecommendationAgent()

    result = agent.run(
        startup_idea,
        idea_analysis,
        market_research,
        competitor_research,
        swot_analysis,
        strategy,
    )

    print("\n===== FINAL RECOMMENDATION =====")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()