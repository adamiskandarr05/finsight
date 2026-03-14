# FinSight — Financial Research Swarm

> **Track A: Intelligence Bureau** · Strategic Research Swarm  
> Gathering, synthesizing, and reasoning over unstructured financial data.

---

## System Architecture — A2A Flow

```
┌─────────────────────────────────────────────────┐
│                   User Query                     │
│         "Analyze NVIDIA Q4 2024 earnings"        │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│           Orchestrator Agent                     │
│   Routes tasks · Merges results · Coordinates   │
└──────┬────────────┬────────────────┬────────────┘
       │            │                │
       ▼            ▼                ▼
┌──────────┐  ┌──────────┐  ┌──────────────┐
│ Scraper  │  │ Analyst  │  │  Reporter    │
│  Agent   │  │  Agent   │  │   Agent      │
│          │  │          │  │              │
│ SEC EDGAR│  │ Trends   │  │ Structures   │
│ News     │  │ Risks    │  │ final brief  │
│ Earnings │  │ Signals  │  │              │
└────┬─────┘  └────┬─────┘  └──────┬───────┘
     │              │               │
     ▼              ▼               ▼
┌─────────────────────────────────────────────────┐
│              Investment Brief                    │
│   Title · Rating · Metrics · Risks · Verdict    │
└─────────────────────────────────────────────────┘
```

---

## Agent Profiles

### 🔍 Scraper Agent (`agents/scraper.py`)
- **Role**: Raw data intelligence gatherer
- **Tools**: Gemini Google Search grounding
- **Gathers**: Recent earnings, SEC filings summaries, news (last 30 days), analyst ratings, key financial metrics (revenue, EPS, P/E, market cap, debt/equity)
- **Output**: Structured JSON with all raw financial data

### 🧠 Analyst Agent (`agents/analyst.py`)
- **Role**: Senior buy-side analyst — reasons over raw data
- **Identifies**: Revenue trends, margin compression/expansion, red flags, bullish signals, valuation vs peers
- **Output**: Structured JSON with trends, risks, signals, synthesis paragraph, confidence level

### 📋 Reporter Agent (`agents/reporter.py`)
- **Role**: Investment brief writer — polishes and structures output
- **Produces**: Rating (BUY/HOLD/SELL/WATCH), key metrics table, risk list, signal list, verdict sentence
- **Output**: Final JSON brief ready for frontend display

### 🎯 Orchestrator (`agents/orchestrator.py`)
- **Role**: Swarm coordinator — sequences agent calls, merges context
- **Pattern**: Sequential fan-out (Scraper → Analyst → Reporter), passes full context forward each step

---

## Directory Structure

```
/agents          — Agent logic (orchestrator, scraper, analyst, reporter)
index.html       — Frontend (HTML/CSS/JS terminal-style UI)
server.py        — Flask API server
requirements.txt
Dockerfile
README.md
```

---

## Setup Instructions

### Prerequisites
- Python 3.12+
- A [Gemini API key](https://aistudio.google.com/app/apikey) (free)

### 1. Clone & Install

```bash
git clone https://github.com/your-username/finsight
cd finsight
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_key_here
```

Or export it directly:
```bash
# macOS/Linux
export GEMINI_API_KEY=your_key_here

# Windows PowerShell
$env:GEMINI_API_KEY = "your_key_here"
```

### 3. Run Locally

**Backend API:**
```bash
python server.py
# Server starts on http://localhost:8080
```

**Frontend:**
The Flask server now serves `index.html` directly at the root. Open `http://localhost:8080` in your browser!

**Run an agent directly (optional test):**
```bash
python agents/orchestrator.py "Analyze Apple AAPL latest earnings"
```

---

## Deploy to Google Cloud Run

### Build & Push

```bash
export PROJECT_ID=your-gcp-project-id

# Build the Docker image
gcloud builds submit --tag gcr.io/$PROJECT_ID/finsight

# Deploy to Cloud Run
gcloud run deploy finsight \
  --image gcr.io/$PROJECT_ID/finsight \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key_here \
  --memory 512Mi \
  --timeout 120
```

### Update Frontend API URL

In `index.html`, update:
```js
const API_BASE = "https://your-cloud-run-url.run.app";
```

Then deploy the frontend via Firebase Hosting, Cloud Storage static site, or any CDN.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Models | Gemini 2.5 Flash |
| Agent Orchestration | Python, google-generativeai SDK |
| Web Search | Gemini Google Search grounding |
| Backend API | Flask + Gunicorn |
| Deployment | Google Cloud Run (Docker) |
| Frontend | Vanilla HTML/CSS/JS |

---

## Example Output

```json
{
  "title": "Apple Inc: Strong Quarter, Services Shine",
  "ticker": "AAPL",
  "rating": "BUY",
  "summary": "Apple delivered strong Q1 2025 results with iPhone beating expectations...",
  "key_metrics": [
    {"label": "Revenue", "value": "$124.3B", "trend": "up"},
    {"label": "EPS",     "value": "$2.40",   "trend": "up"}
  ],
  "risks":   ["China headwinds", "Slowing hardware cycles"],
  "signals": ["Services +14% YoY", "Apple Intelligence driving upgrades"],
  "verdict": "Solid fundamentals with AI tailwinds — BUY at $215 target."
}
```

---

> ⚠️ **Disclaimer**: FinSight is a hackathon project for demonstration purposes only. Nothing produced by this system constitutes financial advice.
