"""
FinSight Analyst Agent
Takes raw scraped data and reasons over it — identifying trends,
red flags, competitive positioning, and investment signals.
"""

import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

ANALYST_SYSTEM = """
You are the FinSight Analyst Agent — a senior buy-side analyst with expertise in
equity research, fundamental analysis, and macroeconomic context.

You will receive raw financial data (earnings, filings, news, metrics) and must:
1. Identify key trends (revenue growth trajectory, margin compression/expansion)
2. Flag risk factors (debt levels, regulatory issues, competitive threats)
3. Highlight bullish signals (new products, partnerships, market share gains)
4. Assess valuation (is the stock cheap/fair/expensive vs peers and history?)
5. Provide a reasoned synthesis paragraph

Return ONLY a JSON object with keys:
  trends: ["...", "..."]
  risk_factors: ["...", "..."]
  bullish_signals: ["...", "..."]
  valuation_assessment: "..."
  synthesis: "2-3 sentence reasoned summary"
  confidence: "high" | "medium" | "low"

No markdown. Valid JSON only.
"""

def run_analyst(query: str, raw_data: dict) -> dict:
    """Synthesize raw data into structured analysis."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=ANALYST_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Original research query: {query}\n\n"
                    f"Raw data gathered by scraper agent:\n"
                    f"{json.dumps(raw_data, indent=2)}\n\n"
                    "Analyze this data and return your structured assessment."
                )
            }
        ]
    )

    raw_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            raw_text += block.text

    clean = raw_text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        return {"raw": raw_text, "error": "parse_failed"}


if __name__ == "__main__":
    sample_data = {
        "earnings": {"revenue": "119.6B", "eps": "2.40", "beat": True},
        "recent_news": ["Apple launches new AI features", "iPhone demand strong in Asia"],
        "key_metrics": {"pe_ratio": 28.5, "market_cap": "3.2T", "debt_to_equity": 1.8}
    }
    result = run_analyst("Analyze Apple AAPL", sample_data)
    print(json.dumps(result, indent=2))
