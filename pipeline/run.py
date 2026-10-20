import sys

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from agents.idea_analyzer import IdeaAnalyzerAgent
from agents.market_researcher import MarketResearchAgent
from agents.competitor_researcher import CompetitorResearchAgent
from agents.swot_risk import SWOTRiskAgent
from agents.strategy_agent import StrategyAgent
from agents.final_recommendation import FinalRecommendationAgent
from agents.report_generator import ReportGeneratorAgent


def run_pipeline(startup_idea: str):

    print("\n" + "=" * 60)
    print("🚀 AI STARTUP IDEA VALIDATOR PIPELINE")
    print("=" * 60)

    # --------------------------------------------------
    # 1. IDEA ANALYSIS
    # --------------------------------------------------

    print("\n[1/7] Running Idea Analyzer...")

    idea_agent = IdeaAnalyzerAgent()
    idea_analysis = idea_agent.run(startup_idea)

    print("✓ Idea Analysis completed")

    # --------------------------------------------------
    # 2. MARKET RESEARCH
    # --------------------------------------------------

    print("\n[2/7] Running Market Researcher...")

    market_agent = MarketResearchAgent()
    market_research = market_agent.run(
        startup_idea,
        idea_analysis.model_dump(),
    )

    print("✓ Market Research completed")

    # --------------------------------------------------
    # 3. COMPETITOR RESEARCH
    # --------------------------------------------------

    print("\n[3/7] Running Competitor Researcher...")

    competitor_agent = CompetitorResearchAgent()
    competitor_research = competitor_agent.run(
        startup_idea,
        idea_analysis.model_dump(),
    )

    print("✓ Competitor Research completed")

    # --------------------------------------------------
    # 4. SWOT & RISK
    # --------------------------------------------------

    print("\n[4/7] Running SWOT & Risk Agent...")

    swot_agent = SWOTRiskAgent()
    swot_analysis = swot_agent.run(
        startup_idea,
        idea_analysis.model_dump(),
        market_research.model_dump(),
        competitor_research.model_dump(),
    )

    print("✓ SWOT & Risk Analysis completed")

    # --------------------------------------------------
    # 5. STRATEGY & MVP
    # --------------------------------------------------

    print("\n[5/7] Running Strategy Agent...")

    strategy_agent = StrategyAgent()
    strategy = strategy_agent.run(
        startup_idea,
        idea_analysis.model_dump(),
        market_research.model_dump(),
        competitor_research.model_dump(),
        swot_analysis.model_dump(),
    )

    print("✓ Strategy & MVP completed")

    # --------------------------------------------------
    # 6. FINAL RECOMMENDATION
    # --------------------------------------------------

    print("\n[6/7] Running Final Recommendation Agent...")

    recommendation_agent = FinalRecommendationAgent()
    final_recommendation = recommendation_agent.run(
        startup_idea,
        idea_analysis.model_dump(),
        market_research.model_dump(),
        competitor_research.model_dump(),
        swot_analysis.model_dump(),
        strategy.model_dump(),
    )

    print("✓ Final Recommendation completed")

    # --------------------------------------------------
    # 7. REPORT GENERATION
    # --------------------------------------------------

    print("\n[7/7] Running Report Generator...")

    report_agent = ReportGeneratorAgent()
    report = report_agent.run(
        startup_idea,
        idea_analysis.model_dump(),
        market_research.model_dump(),
        competitor_research.model_dump(),
        swot_analysis.model_dump(),
        strategy.model_dump(),
        final_recommendation.model_dump(),
    )

    print("✓ Report Generation completed")

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print("\nFINAL VERDICT:")
    print(final_recommendation.verdict)

    print("\nCONFIDENCE:")
    print(final_recommendation.confidence, "/ 10")

    print("\nBIGGEST RISK:")
    print(final_recommendation.biggest_risk)

    print("\nTOP 3 PRIORITIES:")

    for index, priority in enumerate(
        final_recommendation.top_3_priorities,
        start=1,
    ):
        print(f"{index}. {priority}")

    print("\nREPORT:")
    print(report)

    return {
        "startup_idea": startup_idea,
        "idea_analysis": idea_analysis,
        "market_research": market_research,
        "competitor_research": competitor_research,
        "swot_analysis": swot_analysis,
        "strategy": strategy,
        "final_recommendation": final_recommendation,
        "report": report,
    }


def main():

    startup_idea = (
        "An AI platform that helps students discover "
        "and validate startup ideas."
    )

    run_pipeline(startup_idea)


if __name__ == "__main__":
    main()