from ddgs import DDGS

from models.schemas import MarketResearch
from tools.llm import llm_client


class MarketResearchAgent:

    def search_web(self, query: str, max_results: int = 5) -> list[dict]:
        print(f"\nSearching: {query}")

        try:
            results = list(DDGS(timeout=10).text(query, max_results=max_results))
            cleaned_results = []

            for result in results:
                title = result.get("title", "").strip()
                body = result.get("body", "").strip()
                href = result.get("href", "").strip()

                if not title or not body:
                    continue

                cleaned_results.append({
                    "title": title,
                    "snippet": body,
                    "url": href,
                })

            print(f"Found {len(cleaned_results)} results")
            return cleaned_results

        except Exception as e:
            print(f"Search failed: {query}")
            print(f"Reason: {e}")
            print("Found 0 results")
            return []

    def run(self, startup_idea: str, idea_analysis: dict) -> MarketResearch:
        print("\nSearching for market research...")

        industry = idea_analysis.get("industry", "startup technology market")
        target_audience = idea_analysis.get("target_audience", "potential customers")

        queries = [
            f"{industry} market size growth statistics",
            f"{industry} market report CAGR growth",
            f"{industry} market trends {target_audience}",
            f"{startup_idea} market demand",
            f"{startup_idea} industry market competitors",
        ]

        all_results = []
        seen_urls = set()

        for query in queries:
            results = self.search_web(query)

            for result in results:
                url = result.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append(result)

        print(f"\nTotal unique market research results: {len(all_results)}")

        unavailable = "Not available from provided web evidence."

        if not all_results:
            return MarketResearch(
                total_addressable_market=unavailable,
                serviceable_addressable_market=unavailable,
                serviceable_obtainable_market=unavailable,
                market_growth_rate=unavailable,
                key_trends=[],
                opportunities=[],
                market_maturity="Unknown",
                summary="No reliable web evidence was available for this market.",
            )

        evidence_text = "\n\n".join(
            f"SOURCE [{index}]\n"
            f"TITLE: {item['title']}\n"
            f"SNIPPET: {item['snippet']}\n"
            f"SOURCE URL: {item['url']}"
            for index, item in enumerate(all_results, start=1)
        )

        system_prompt = """
You are a strict evidence-based market research analyst.

Use ONLY the web evidence supplied by the user.
Do not use your own knowledge.
Do not invent facts.
Do not estimate or calculate values.

TAM:
Only use a value explicitly identified as Total Addressable Market (TAM).
If valid, the value MUST start with "TAM:".
A general market size is NOT automatically TAM.

SAM:
Only use a value explicitly identified as Serviceable Addressable Market (SAM).
If valid, the value MUST start with "SAM:".
A general market size is NOT automatically SAM.

SOM:
Only use a value explicitly identified as Serviceable Obtainable Market (SOM).
If valid, the value MUST start with "SOM:".
A general market forecast is NOT automatically SOM.

If TAM, SAM, or SOM is not explicitly supported, return:
"Not available from provided web evidence."

MARKET GROWTH:
Select ONE representative growth rate only.
It must contain an actual percentage.
Never combine multiple CAGR values.
If no reliable percentage is available, return:
"Not available from provided web evidence."

MARKET MATURITY:
Use only Emerging, Growing, Mature, Declining, or Unknown.

Every numerical claim must be directly supported by the supplied evidence.
"""

        user_prompt = f"""
Startup idea:
{startup_idea}

Industry:
{industry}

Target audience:
{target_audience}

WEB EVIDENCE:

{evidence_text}

Return structured market research.

TAM:
Only use explicitly identified TAM. If valid, start with "TAM:".
Otherwise return "Not available from provided web evidence."

SAM:
Only use explicitly identified SAM. If valid, start with "SAM:".
Otherwise return "Not available from provided web evidence."

SOM:
Only use explicitly identified SOM. If valid, start with "SOM:".
Otherwise return "Not available from provided web evidence."

Market growth rate:
Select exactly ONE reliable percentage from the strongest relevant source.
Example: "17.34% CAGR (2026-2035) [SOURCE 2]"

Key trends:
Only evidence-supported trends.

Opportunities:
Only evidence-supported opportunities.

Market maturity:
Choose Emerging, Growing, Mature, Declining, or Unknown.

Summary:
Do not introduce any new number, market size, CAGR, percentage, or projection.
Do not invent facts.
"""

        try:
            result = llm_client.generate_structured(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_model=MarketResearch,
            )
        except Exception as e:
            print(f"\nStructured market research failed: {e}")
            return MarketResearch(
                total_addressable_market=unavailable,
                serviceable_addressable_market=unavailable,
                serviceable_obtainable_market=unavailable,
                market_growth_rate=unavailable,
                key_trends=[],
                opportunities=[],
                market_maturity="Unknown",
                summary="Market research could not be reliably generated from the available web evidence.",
            )

        # DATA QUALITY VALIDATION
        if "%" not in (result.market_growth_rate or ""):
            result.market_growth_rate = unavailable

        tam = result.total_addressable_market or ""
        sam = result.serviceable_addressable_market or ""
        som = result.serviceable_obtainable_market or ""

        if not (tam.lower().startswith("tam:") or "total addressable market:" in tam.lower()):
            result.total_addressable_market = unavailable

        if not (sam.lower().startswith("sam:") or "serviceable addressable market:" in sam.lower()):
            result.serviceable_addressable_market = unavailable

        if not (som.lower().startswith("som:") or "serviceable obtainable market:" in som.lower()):
            result.serviceable_obtainable_market = unavailable

        # Build summary ourselves so unsupported numbers cannot be added.
        summary_parts = []

        if result.market_growth_rate != unavailable:
            summary_parts.append(
                f"Web evidence indicates a market growth rate of {result.market_growth_rate}."
            )

        if result.market_maturity != "Unknown":
            summary_parts.append(
                f"The market is classified as {result.market_maturity.lower()}."
            )

        if result.key_trends:
            trends = [item.trend for item in result.key_trends[:3] if item.trend]
            if trends:
                summary_parts.append("Key trends include " + ", ".join(trends) + ".")

        if result.opportunities:
            opportunities = [item for item in result.opportunities[:3] if item]
            if opportunities:
                summary_parts.append(
                    "Potential opportunities include " + ", ".join(opportunities) + "."
                )

        result.summary = (
            " ".join(summary_parts)
            if summary_parts
            else "The available web evidence does not provide enough reliable information for a detailed market summary."
        )

        return result


if __name__ == "__main__":
    startup_idea = (
        "An AI platform that helps students discover "
        "and validate startup ideas."
    )

    idea_analysis = {
        "industry": "Education Technology",
        "target_audience": "Students",
    }

    agent = MarketResearchAgent()
    result = agent.run(startup_idea, idea_analysis)

    print("\n===== MARKET RESEARCH =====")
    print(result.model_dump_json(indent=2))
