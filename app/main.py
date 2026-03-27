from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.db import get_session, init_db
from app.models import FeedbackRequest, ImproveRequest, ImproveResponse, PromptRecord, TestRequest, TestResponse
from app.services.model_client import ModelClient
from app.services.prompt_pipeline import MultiAgentPromptFixer, validate_instruction_following

app = FastAPI(title="Prompt Fixer")
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

pipeline = MultiAgentPromptFixer()
model_client = ModelClient()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/improve", response_model=ImproveResponse)
def improve_prompt(payload: ImproveRequest):
    improved, consensus_reached, notes = pipeline.run(payload.prompt)
    return ImproveResponse(improved_prompt=improved, consensus_reached=consensus_reached, agent_notes=notes)


@app.post("/api/test", response_model=TestResponse)
def test_prompt(payload: TestRequest):
    output = model_client.generate(payload.improved_prompt, payload.model)
    ok, notes = validate_instruction_following(payload.improved_prompt, output)
    return TestResponse(output=output, instruction_followed=ok, validation_notes=notes)


@app.post("/api/feedback")
def store_feedback(payload: FeedbackRequest, session: Session = Depends(get_session)):
    record = PromptRecord(**payload.model_dump())
    session.add(record)
    session.commit()
    session.refresh(record)
    return {"status": "ok", "id": record.id}


@app.get("/api/feedback")
def list_feedback(session: Session = Depends(get_session)):
    rows = session.query(PromptRecord).order_by(PromptRecord.created_at.desc()).limit(100).all()
    return {"items": rows}
