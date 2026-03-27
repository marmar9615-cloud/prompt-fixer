from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from app.db import get_session
from app.main import app


def test_feedback_storage_roundtrip():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    def override_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    client = TestClient(app)

    payload = {
        "original_prompt": "Explain photosynthesis",
        "improved_prompt": "Role: ...",
        "model_name": "gpt-4o-mini",
        "model_output": "Answer: ... Evidence: ... Caveats: ...",
        "rating": 4,
        "rank": 1,
    }

    post = client.post("/api/feedback", json=payload)
    assert post.status_code == 200
    assert post.json()["status"] == "ok"

    get = client.get("/api/feedback")
    assert get.status_code == 200
    assert len(get.json()["items"]) == 1
    assert get.json()["items"][0]["rating"] == 4
