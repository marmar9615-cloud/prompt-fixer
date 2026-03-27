# Prompt Fixer

Research-backed Prompt Fixer web app that improves prompts, runs a multi-agent hallucination reduction workflow, tests outputs against selected models, and stores user ratings for future learning.

## Features

- Prompt input interface.
- Multi-agent prompt improvement workflow (writer, editor, proof-reader, fact-checker).
- Improved prompt preview + consensus status.
- Model test execution endpoint.
- Instruction-following validation step.
- Feedback storage (prompt/output/rating/rank) in SQLite.
- Automated tests for core workflows.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>.

> Optional: set `OPENAI_API_KEY` for live model calls. Otherwise, the app runs in demo mode.

## Run tests

```bash
pytest -q
```

## Files

- `RESEARCH_REPORT.md`: planning and research summary with sources.
- `app/`: FastAPI application and multi-agent services.
- `tests/`: automated tests.
