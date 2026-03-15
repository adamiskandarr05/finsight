"""
FinSight Tools — JSON Utilities
Shared helper for cleaning and parsing LLM JSON responses.
"""

import json


def parse_llm_json(raw_text: str) -> dict:
    """
    Strip markdown code fences from an LLM response and parse as JSON.
    Returns the parsed dict, or {'raw': raw_text, 'error': 'parse_failed'} on failure.
    """
    clean = raw_text.strip()

    # Strip opening fence
    if clean.startswith("```json"):
        clean = clean[len("```json"):]
    elif clean.startswith("```"):
        clean = clean[len("```"):]

    # Strip closing fence
    if clean.endswith("```"):
        clean = clean[:-len("```")]

    clean = clean.strip()

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        return {"raw": raw_text, "error": "parse_failed"}
