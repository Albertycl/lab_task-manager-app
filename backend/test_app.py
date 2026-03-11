import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"


def test_get_tasks(client):
    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_create_task(client):
    resp = client.post("/api/tasks", json={"title": "Test task"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["title"] == "Test task"
    assert data["done"] is False


def test_create_task_no_title(client):
    resp = client.post("/api/tasks", json={})
    assert resp.status_code == 400


def test_update_task(client):
    resp = client.patch("/api/tasks/1", json={"done": True})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["done"] is True


def test_delete_task(client):
    # Create one first
    resp = client.post("/api/tasks", json={"title": "To delete"})
    task_id = resp.get_json()["id"]
    # Delete it
    resp = client.delete(f"/api/tasks/{task_id}")
    assert resp.status_code == 200
