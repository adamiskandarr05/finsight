"""
FinSight Reporter Agent
Takes analyst output and structures it into a clean, final investment brief
suitable for display in the frontend.
"""

import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

REPORTER_SYSTEM = """
You are the FinSight Reporter Agent. You write clear, concise investment briefs
for professional and retail investors.

Given a query and analyst assessment, produce a polished final brief.

Return ONLY a JSON object with these exact keys:
  title: "Company Name: Brief Title (e.g. Strong Quarter, Cautious Outlook)"
  ticker: "TICKER"
  rating: "BUY" | "HOLD" | "SELL" | "WATCH"
  summary: "2-3 sentence executive summary"
  key_metrics: [
    {label: "Revenue", value: "...", trend: "up" | "down" | "flat"},
    {label: "EPS", value: "...", trend: "up" | "down" | "flat"},
    {label: "P/E Ratio", value: "...", trend: "up" | "down" | "flat"},
    {label: "Market Cap", value: "...", trend: "up" | "down" | "flat"}
  ]
  risks: ["...", "...", "..."]
  signals: ["...", "...", "..."]
  verdict: "One punchy sentence with the investment conclusion"
  generated_at: "ISO timestamp placeholder"

No markdown. Valid JSON only.
"""

def run_reporter(query: str, analysis: dict) -> dict:
    """Produce the final structured investment brief."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1200,
        system=REPORTER_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Original query: {query}\n\n"
                    f"Analyst assessment:\n{json.dumps(analysis, indent=2)}\n\n"
                    "Generate the final investment brief."
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
        data = json.loads(clean)
        # Inject timestamp
        from datetime import datetime, timezone
        data["generated_at"] = datetime.now(timezone.utc).isoformat()
        return data
    except json.JSONDecodeError:
        return {"raw": raw_text, "error": "parse_failed"}


if __name__ == "__main__":
    sample_analysis = {
        "trends": ["Revenue grew 6% YoY", "Services segment accelerating"],
        "risk_factors": ["China headwinds", "AI competition"],
        "bullish_signals": ["New AI integrations", "Strong buybacks"],
        "synthesis": "Apple continues to demonstrate resilient fundamentals.",
        "confidence": "high"
    }
    result = run_reporter("Analyze Apple AAPL", sample_analysis)
    print(json.dumps(result, indent=2))
