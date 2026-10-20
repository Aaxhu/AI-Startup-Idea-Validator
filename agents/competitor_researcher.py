from ddgs import DDGS

from models.schemas import CompetitorResearch, Competitor
from tools.llm import llm_client


class CompetitorResearchAgent:

    def generate_queries(
        self,
        startup_idea: str,
        idea_analysis: dict | None = None
    ) -> list[str]:
        if not idea_analysis:
            idea_analysis = {}

        industry = idea_analysis.get("industry", "").strip()
        category = idea_analysis.get("startup_category", "").strip()
        audience = idea_analysis.get("target_audience", "").strip()
        pain_point = idea_analysis.get("customer_pain_point", "").strip()
        value_prop = idea_analysis.get("value_proposition", "").strip()

        queries = []

        # 1. Category / industry software platforms
        if industry and category and industry.lower() != category.lower():
            queries.append(f"{industry} {category} software platforms")
        elif industry:
            queries.append(f"{industry} software platform tools")
        elif category:
            queries.append(f"{category} software platform tools")

        # 2. Value proposition / solution
        if value_prop:
            first_val = value_prop.split(",")[0].strip()
            queries.append(f"{first_val} software platform")

        # 3. Core concept from idea
        core = startup_idea
        for prefix in (
            "an ai platform for ",
            "an ai platform that ",
            "a platform for ",
            "a platform that ",
            "an app that ",
            "an app for ",
            "a saas for ",
            "a tool that ",
        ):
            if core.lower().startswith(prefix):
                core = core[len(prefix):]
                break
        words = core.split()
        short_concept = " ".join(words[:6])
        if short_concept:
            queries.append(f"{short_concept} software competitors")
            queries.append(f"{short_concept} platforms")

        # 4. Audience tools
        if audience and (industry or category):
            queries.append(f"{industry or category} tools for {audience}")

        # Fallback if queries is empty
        if not queries:
            queries.append(f"{startup_idea[:60]} competitors")

        # Deduplicate while preserving order
        unique_queries = []
        seen = set()
        for q in queries:
            q_clean = q.strip()
            if q_clean and q_clean.lower() not in seen:
                seen.add(q_clean.lower())
                unique_queries.append(q_clean)

        return unique_queries[:5]

    def search_web(
        self,
        startup_idea: str,
        idea_analysis: dict | None = None
    ) -> list[dict]:

        queries = self.generate_queries(startup_idea, idea_analysis)

        results = []

        for query in queries:
            try:
                print(f"\nSearching: {query}")

                search_results = list(
                    DDGS(timeout=10).text(
                        query,
                        max_results=5
                    )
                )

                print(f"Found {len(search_results)} results")
                results.extend(search_results)

            except Exception as e:
                print(f"Search failed: {query}")
                print(f"Reason: {e}")

        unique_results = []
        seen_urls = set()

        for result in results:
            url = result.get("href", "").strip()

            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)

        return unique_results[:30]

    def is_product_page(self, result: dict) -> bool:

        title = result.get("title", "").strip().lower()
        url = result.get("href", "").strip().lower()

        excluded_title_patterns = [
            "best startup idea",
            "best idea validation",
            "idea validation tools",
            "top validation tools",
            "tools tested",
            "tools (2026)",
            "tools in 2026",
            "comparison",
            "list of",
            "alternatives",
            "guide to",
            "how to",
        ]

        if any(
            pattern in title
            for pattern in excluded_title_patterns
        ):
            return False

        excluded_url_patterns = [
            "/blog/",
            "/blogs/",
            "/list/",
            "/lists/",
            "/article/",
            "/articles/",
            "/guide/",
            "/guides/",
        ]

        if any(
            pattern in url
            for pattern in excluded_url_patterns
        ):
            return False

        return True

    def build_candidates(
        self,
        search_results: list[dict],
        idea_analysis: dict | None = None,
        startup_idea: str = ""
    ) -> list[dict]:

        candidates = []
        seen_names = set()

        product_indicators = {
            "platform", "software", "app", "tool", "solution",
            "system", "service", "ai", "product", "saas", "dashboard"
        }

        topic_keywords = set()
        if idea_analysis:
            for field in ("industry", "startup_category", "target_audience", "customer_pain_point"):
                val = idea_analysis.get(field, "")
                if val:
                    for w in val.lower().split():
                        cleaned = "".join(c for c in w if c.isalnum())
                        if len(cleaned) >= 3:
                            topic_keywords.add(cleaned)

        if startup_idea:
            for w in startup_idea.lower().split():
                cleaned = "".join(c for c in w if c.isalnum())
                if len(cleaned) >= 4 and cleaned not in (
                    "about", "their", "which", "where", "there", "these", "those", "based"
                ):
                    topic_keywords.add(cleaned)

        relevant_keywords = product_indicators | topic_keywords

        for result in search_results:

            title = result.get("title", "").strip()
            url = result.get("href", "").strip()
            body = result.get("body", "").strip()

            if not title or not url:
                continue

            if not self.is_product_page(result):
                continue

            text = f"{title} {body}".lower()

            if not any(
                keyword in text
                for keyword in relevant_keywords
            ):
                continue

            key = title.lower()

            if key in seen_names:
                continue

            seen_names.add(key)

            candidates.append(
                {
                    "name": title,
                    "website": url,
                    "description": body[:500]
                    if body
                    else "No description available.",
                }
            )

            if len(candidates) >= 15:
                break

        return candidates

    def make_competitor(
        self,
        candidate: dict
    ) -> Competitor:

        return Competitor(
            name=candidate["name"],
            website=candidate["website"],
            description=candidate["description"],
            strengths=[],
            weaknesses=[],
            funding_stage=None,
            approximate_users_or_revenue=None,
        )

    def run(
        self,
        startup_idea: str,
        idea_analysis: dict
    ) -> CompetitorResearch:

        print("\nSearching for competitors...")

        search_results = self.search_web(startup_idea, idea_analysis)

        print(
            f"\nTotal unique search results: "
            f"{len(search_results)}"
        )

        candidates = self.build_candidates(
            search_results,
            idea_analysis,
            startup_idea
        )

        print(
            f"Verified product candidates: "
            f"{len(candidates)}"
        )

        if not candidates:

            return CompetitorResearch(
                direct_competitors=[],
                indirect_competitors=[],
                market_gaps=[],
                competitive_intensity="Unknown",
                differentiation_opportunities=[],
                summary=(
                    "No relevant product competitors were "
                    "identified from the available web results."
                ),
            )

        candidate_text = ""

        for index, candidate in enumerate(
            candidates,
            start=1
        ):

            candidate_text += (
                f"\nCandidate {index}\n"
                f"Name: {candidate['name']}\n"
                f"URL: {candidate['website']}\n"
                f"Description: {candidate['description']}\n"
            )

        system_prompt = """
You are a strict evidence-based competitor analyst.

Use ONLY the supplied candidate list.

IMPORTANT:
- Never invent a company.
- Never invent a competitor name.
- Never invent a URL.
- Never invent funding.
- Never invent revenue.
- Never invent user numbers.
- Never invent strengths.
- Never invent weaknesses.

Only use competitor names that exactly match the supplied
candidate names.

DIRECT COMPETITOR:
A product that directly validates, evaluates, analyzes,
tests, or develops startup/business ideas.

INDIRECT COMPETITOR:
A broader product that provides entrepreneurship, business,
market research, or startup analysis but is not primarily a
startup-idea validation product.

Do not put the same competitor in both categories.

For funding_stage and approximate_users_or_revenue:
return null unless explicitly supported by the candidate
description.

For strengths and weaknesses:
return empty lists unless directly supported by the
candidate description.

For market_gaps and differentiation_opportunities:
return empty lists unless they can be directly supported
by the supplied competitor descriptions.

Do not infer weaknesses merely because information is absent.

Return structured data only.
"""

        user_prompt = f"""
Startup idea:
{startup_idea}

Industry:
{idea_analysis.get("industry", "")}

Target audience:
{idea_analysis.get("target_audience", "")}

Customer pain point:
{idea_analysis.get("customer_pain_point", "")}

VERIFIED PRODUCT CANDIDATES:
{candidate_text}

Classify the candidates.

Maximum:
- 5 direct competitors
- 5 indirect competitors

Only use exact candidate names.

Do not invent additional information.

If the evidence does not support market gaps or
differentiation opportunities, return empty lists.
"""

        try:

            result = llm_client.generate_structured(
                system_prompt,
                user_prompt,
                CompetitorResearch
            )

        except Exception as e:

            print(
                f"\nLLM competitor analysis failed: {e}"
            )

            result = CompetitorResearch(
                direct_competitors=[],
                indirect_competitors=[],
                market_gaps=[],
                competitive_intensity="Unknown",
                differentiation_opportunities=[],
                summary=(
                    "Competitor classification could not be "
                    "reliably generated from the available "
                    "web evidence."
                ),
            )

        candidate_lookup = {
            candidate["name"].lower(): candidate
            for candidate in candidates
        }

        def validate(
            competitors: list[Competitor]
        ) -> list[Competitor]:

            validated = []
            seen = set()

            for competitor in competitors:

                key = competitor.name.strip().lower()

                if key not in candidate_lookup:
                    continue

                if key in seen:
                    continue

                seen.add(key)

                candidate = candidate_lookup[key]

                validated.append(
                    self.make_competitor(candidate)
                )

                if len(validated) >= 5:
                    break

            return validated

        direct = validate(
            result.direct_competitors
        )

        indirect = validate(
            result.indirect_competitors
        )

        # ---------------------------------------------------------
        # Deterministic correction:
        # Products matching the core value proposition or pain
        # points are treated as direct competitors.
        # ---------------------------------------------------------

        solution_keywords = set()
        if idea_analysis:
            val = idea_analysis.get("value_proposition", "")
            if val:
                solution_keywords.update(
                    [p.strip().lower() for p in val.split(",") if len(p.strip()) > 3]
                )
            pain = idea_analysis.get("customer_pain_point", "")
            if pain:
                solution_keywords.update(
                    [p.strip().lower() for p in pain.split(",") if len(p.strip()) > 3]
                )

        direct_keys = {
            competitor.name.lower()
            for competitor in direct
        }

        indirect_keys = {
            competitor.name.lower()
            for competitor in indirect
        }

        if solution_keywords:
            for candidate in candidates:

                text = (
                    candidate["name"] + " "
                    + candidate["description"]
                ).lower()

                if any(
                    keyword in text
                    for keyword in solution_keywords
                ):

                    key = candidate["name"].lower()

                    if key not in direct_keys:

                        direct.append(
                            self.make_competitor(candidate)
                        )

                        direct_keys.add(key)

                    if key in indirect_keys:

                        indirect = [
                            competitor
                            for competitor in indirect
                            if competitor.name.lower() != key
                        ]

                        indirect_keys.discard(key)

                    if len(direct) >= 5:
                        break

        # ---------------------------------------------------------
        # Remove duplicates between direct and indirect.
        # ---------------------------------------------------------

        direct_keys = {
            competitor.name.lower()
            for competitor in direct
        }

        indirect = [
            competitor
            for competitor in indirect
            if competitor.name.lower() not in direct_keys
        ]

        # ---------------------------------------------------------
        # If classification produced nothing, use the strongest
        # verified candidates as fallback.
        # ---------------------------------------------------------

        if not direct and not indirect:

            print(
                "\nNo classified competitors returned. "
                "Using verified search candidates."
            )

            direct = [
                self.make_competitor(candidate)
                for candidate in candidates[:5]
            ]

        # ---------------------------------------------------------
        # Evidence-based competitive intensity.
        # ---------------------------------------------------------

        competitor_count = (
            len(direct) + len(indirect)
        )

        if competitor_count >= 5:
            intensity = "High"
        elif competitor_count >= 2:
            intensity = "Medium"
        elif competitor_count == 1:
            intensity = "Low"
        else:
            intensity = "Unknown"

        # We intentionally do not invent market gaps or
        # differentiation claims without explicit evidence.
        result.direct_competitors = direct[:5]
        result.indirect_competitors = indirect[:5]
        result.market_gaps = []
        result.differentiation_opportunities = []
        result.competitive_intensity = intensity

        total = (
            len(result.direct_competitors)
            + len(result.indirect_competitors)
        )

        result.summary = (
            f"{total} verified competitor products were "
            f"identified from live web search. "
            f"Competitor names, URLs, and descriptions are "
            f"grounded in retrieved search results."
        )

        return result


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

    agent = CompetitorResearchAgent()

    result = agent.run(
        startup_idea,
        idea_analysis
    )

    print("\n===== COMPETITOR RESEARCH =====")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
