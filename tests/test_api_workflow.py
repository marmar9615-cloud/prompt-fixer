from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_improve_then_test_flow_demo_mode():
    improve = client.post("/api/improve", json={"prompt": "Summarize quarterly revenue trends"})
    assert improve.status_code == 200
    improved_prompt = improve.json()["improved_prompt"]
    assert improve.json()["consensus_reached"] is True

    run = client.post("/api/test", json={"improved_prompt": improved_prompt, "model": "gpt-4o-mini"})
    assert run.status_code == 200
    body = run.json()
    assert "Answer:" in body["output"]
    assert "Evidence:" in body["output"]
    assert "Caveats:" in body["output"]
