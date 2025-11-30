# Senior QA Automation Exercise - Quick Start

## Quick Start

```bash
cd brighthive-testing-exercise/senior_qa_exercise
./start.sh
```

The webapp will be running at **http://localhost:8000**

**Swagger UI**: http://localhost:8000/docs ← **You must automate this!**

## Manual Setup

```bash
cd brighthive-testing-exercise/senior_qa_exercise

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the webapp
python webapp.py
# Or: uvicorn webapp:app --reload --port 8000
```

## Access Points

- **Swagger UI:** http://localhost:8000/docs ← **Automate this with Playwright/Cypress/Selenium**
- **Health Check:** http://localhost:8000/health

## For Candidates

See `CANDIDATE_INSTRUCTIONS.md` for the full exercise details.

## For Interviewers

See `EVALUATION_CRITERIA.md` for evaluation guidelines.
