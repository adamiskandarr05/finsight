"""
FinSight Scraper Agent
Uses Gemini with Google Search grounding to gather: SEC filings, earnings data,
recent news, and analyst commentary for a given company/query.
"""

import os
import json
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

SCRAPER_SYSTEM = """
You are the FinSight Scraper Agent. Your role is to gather raw financial intelligence.

For the given query, use web search to collect:
- Recent earnings reports (revenue, EPS, guidance)
- SEC filings highlights (10-K, 10-Q if relevant)
- Recent news (last 30 days) affecting the company or sector
- Analyst ratings and price targets
- Key financial metrics (P/E, market cap, debt levels)

Return ONLY a JSON object with keys:
  earnings: {...}
  filings_summary: "..."
  recent_news: ["...", "..."]
  analyst_ratings: [{analyst, rating, target}]
  key_metrics: {revenue, eps, pe_ratio, market_cap, debt_to_equity}

No markdown. No preamble. Valid JSON only.
"""



def run_scraper(query: str) -> dict:
    """Run the scraper agent, returns raw financial data as dict."""

    # Correct Google Search grounding instantiation for the new SDK
    search_tool = genai.protos.Tool(
        google_search=genai.protos.Tool.GoogleSearch()
    )

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SCRAPER_SYSTEM,
        tools=[search_tool]
    )

    response = model.generate_content(
        f"Research this financial query and gather all available data: {query}"
    )

    raw_text = response.text

    # Clean and parse JSON
    clean = raw_text.strip()
    if clean.startswith("```json"):
        clean = clean[len("```json"):]
    elif clean.startswith("```"):
        clean = clean[len("```"):]
    if clean.endswith("```"):
        clean = clean[:-len("```")]
    clean = clean.strip()

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        return {"raw": raw_text, "error": "parse_failed"}


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "Apple AAPL latest earnings"
    result = run_scraper(q)
    print(json.dumps(result, indent=2))
