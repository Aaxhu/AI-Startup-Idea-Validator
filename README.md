# AI Startup Idea Validator

An AI-powered platform that helps entrepreneurs evaluate startup ideas through market research, competitor analysis, SWOT and risk assessment, MVP planning, and AI-driven recommendations.

## Features

- **Idea Analysis:** Evaluate startup concepts.
- **Market Research:** Explore market trends and opportunities.
- **Competitor Analysis:** Identify competitors and positioning.
- **SWOT & Risk Assessment:** Examine strengths, weaknesses, opportunities, and threats.
- **MVP & Strategy:** Plan essential features and revenue models.
- **Final Recommendation:** Generate an evidence-informed startup verdict.
- **Report Generation:** Produce a structured validation report.

## Tech Stack

- Python
- Streamlit
- FastAPI
- Ollama
- Pydantic
- Multi-agent AI pipeline

## Run Locally

Clone the repository:

```bash
git clone https://github.com/Aaxhu/AI-Startup-Idea-Validator.git
cd AI-Startup-Idea-Validator
```

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
```

On Windows Git Bash:

```bash
source .venv/Scripts/activate
pip install -r requirements.txt
```

Start the backend in one terminal:

```bash
python -m uvicorn app.main:app --reload
```

Start the frontend in a second terminal:

```bash
python -m streamlit run ui/app.py
```

The frontend and backend must be running, and Ollama must be configured and reachable for AI inference.

## Project Structure

- `agents/` — AI agents
- `app/` — FastAPI backend
- `models/` — Data schemas
- `pipeline/` — Validation workflow
- `tests/` — Tests
- `tools/` — Supporting utilities
- `ui/` — Streamlit interface

## Note

This project is intended to support startup decision-making. Its recommendations should be evaluated against reliable market evidence and real-world customer research.
