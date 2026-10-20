from tools.llm import llm_client
from models.schemas import IdeaAnalysis


class IdeaAnalyzerAgent:
    """
    Analyzes a startup idea and converts it into
    a structured IdeaAnalysis object.
    """

    def run(self, startup_idea: str) -> IdeaAnalysis:
        system_prompt = """
You are a professional startup idea analyst.

Analyze the startup idea carefully.

Return ONLY valid JSON.
Do not use Markdown.
Do not add explanations outside the JSON.

The JSON must contain exactly these fields:

{
  "industry": "string",
  "target_audience": "string",
  "customer_pain_point": "string",
  "value_proposition": "string",
  "startup_category": "string",
  "key_assumptions": ["string"],
  "feasibility_score": 1,
  "summary": "string"
}

Rules:
- feasibility_score must be an integer from 1 to 10.
- key_assumptions must be a JSON array.
- Every required field must be present.
- Do not return null for required fields.
"""

        user_prompt = f"""
Analyze this startup idea:

{startup_idea}
"""

        return llm_client.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=IdeaAnalysis,
        )


# Simple test helper
if __name__ == "__main__":
    agent = IdeaAnalyzerAgent()

    idea = (
        "An AI platform that helps students discover "
        "and validate startup ideas."
    )

    result = agent.run(idea)

    print("\n===== IDEA ANALYSIS =====")
    print(result.model_dump_json(indent=2))