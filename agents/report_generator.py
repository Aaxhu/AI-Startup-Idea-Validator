from pathlib import Path
from datetime import datetime

from tools.llm import llm_client


class ReportGeneratorAgent:

    def run(
        self,
        startup_idea: str,
        idea_analysis: dict,
        market_research: dict,
        competitor_research: dict,
        swot_analysis: dict,
        strategy: dict,
        final_recommendation: dict,
    ) -> str:

        system_prompt = """
You are a professional startup evaluation report writer.

Create a clear, professional startup validation report
using ONLY the information provided.

Do not invent statistics, companies, funding information,
market values, or other facts.

Use Markdown formatting.

The report must contain:

1. Executive Summary
2. Startup Idea Analysis
3. Market Analysis
4. Competitor Analysis
5. SWOT Analysis
6. MVP & Business Strategy
7. Final Recommendation
8. Key Risks
9. Next Steps

Make the report practical and easy to understand.
"""

        user_prompt = f"""
STARTUP IDEA
============

{startup_idea}


IDEA ANALYSIS
=============

{idea_analysis}


MARKET RESEARCH
===============

{market_research}


COMPETITOR RESEARCH
===================

{competitor_research}


SWOT & RISK ANALYSIS
====================

{swot_analysis}


MVP & STRATEGY
==============

{strategy}


FINAL RECOMMENDATION
====================

{final_recommendation}


Generate the complete startup validation report.

Important:
- Use the provided information only.
- Do not invent missing data.
- Clearly mention when information is unavailable.
- Keep recommendations actionable.
- Return Markdown text only.
"""

        report = llm_client.generate(
            system_prompt,
            user_prompt,
        )

        return report


def save_report(report: str) -> str:

    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = reports_dir / f"startup_validation_{timestamp}.md"

    report_path.write_text(
        report,
        encoding="utf-8",
    )

    return str(report_path)


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
        "feasibility_score": 8,
        "summary": (
            "The platform can help students evaluate startup "
            "ideas using AI-powered analysis."
        ),
    }

    market_research = {
        "summary": (
            "Growing opportunity for AI-powered education "
            "and startup validation tools."
        ),
        "market_maturity": "Growing",
        "opportunities": [
            "AI-powered education tools",
            "Student entrepreneurship",
            "Startup validation services",
        ],
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
        "summary": (
            "There are existing startup validation tools, "
            "but opportunities exist for deeper market and "
            "strategy analysis."
        ),
    }

    swot_analysis = {
        "strengths": [
            "AI-powered recommendations",
            "Student-focused platform",
            "Market and competitor analysis",
        ],
        "weaknesses": [
            "Dependence on accurate data",
            "Competition from existing tools",
        ],
        "opportunities": [
            "Growing interest in AI tools",
            "Student entrepreneurship",
            "Educational partnerships",
        ],
        "threats": [
            "Existing competitors",
            "Incorrect recommendations from inaccurate data",
        ],
        "overall_viability": "High",
        "key_risk": (
            "Dependence on accurate data for recommendations"
        ),
        "summary": (
            "Strong potential with data-quality and "
            "competition risks."
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
        "growth_plan": "Aggressive",
        "summary": (
            "Focus on students, AI-powered idea validation, "
            "and market research."
        ),
    }

    final_recommendation = {
        "verdict": "GO WITH CHANGES",
        "confidence": 7,
        "rationale": (
            "The platform has strong potential but faces "
            "competition and data-quality risks."
        ),
        "top_3_priorities": [
            "Implement a robust market research tool",
            "Develop a comprehensive competitor analysis framework",
            "Establish a student-focused go-to-market strategy",
        ],
        "biggest_risk": (
            "Dependence on accurate data for recommendations"
        ),
    }

    agent = ReportGeneratorAgent()

    report = agent.run(
        startup_idea,
        idea_analysis,
        market_research,
        competitor_research,
        swot_analysis,
        strategy,
        final_recommendation,
    )

    report_path = save_report(report)

    print("\n===== STARTUP VALIDATION REPORT =====\n")
    print(report)

    print("\n===== REPORT SAVED =====")
    print(report_path)


if __name__ == "__main__":
    main()