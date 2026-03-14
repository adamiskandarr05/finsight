"""
FinSight Scraper Agent
Uses Claude's web_search tool to gather: SEC filings, earnings data,
recent news, and analyst commentary for a given company/query.
"""

import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

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

SEARCH_TOOL = {
    "type": "web_search_20250305",
    "name": "web_search"
}

def run_scraper(query: str) -> dict:
    """Run the scraper agent, returns raw financial data as dict."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=SCRAPER_SYSTEM,
        tools=[SEARCH_TOOL],
        messages=[
            {
                "role": "user",
                "content": f"Research this financial query and gather all available data: {query}"
            }
        ]
    )

    # Extract text from response (may go through tool use rounds)
    raw_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            raw_text += block.text

    # Clean and parse JSON
    clean = raw_text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        # Return partial data if parsing fails
        return {"raw": raw_text, "error": "parse_failed"}


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "Apple AAPL latest earnings"
    result = run_scraper(q)
    print(json.dumps(result, indent=2))
