
from fastapi.testclient import TestClient
from app import main as main_module

client = TestClient(main_module.app)


def mock_intent(monkeypatch, intent):
    monkeypatch.setattr(
        main_module,
        "interpret_question",
        lambda question: {
            "intent": intent,
            "month1": None,
            "month2": None
        }
    )


def test_total_revenue(monkeypatch):
    mock_intent(monkeypatch, "total_revenue")

    response = client.post(
        "/ask",
        json={"question": "What is the total revenue?"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["supporting_data"]["total_revenue"] == 1439200
    assert data["supporting_data"]["transactions"] == 48


def test_top_product(monkeypatch):
    mock_intent(monkeypatch, "top_product")

    response = client.post(
        "/ask",
        json={"question": "Which product generated the highest revenue?"}
    )

    assert response.status_code == 200
    assert "Monitor" in response.json()["answer"]


def test_top_region(monkeypatch):
    mock_intent(monkeypatch, "top_region")

    response = client.post(
        "/ask",
        json={"question": "Which region has the highest sales?"}
    )

    assert response.status_code == 200
    assert "South" in response.json()["answer"]


def test_monthly_trend(monkeypatch):
    mock_intent(monkeypatch, "monthly_trend")

    response = client.post(
        "/ask",
        json={"question": "Show monthly revenue trend"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["supporting_data"]) == 6


def test_unsupported_question(monkeypatch):
    mock_intent(monkeypatch, "unsupported")

    response = client.post(
        "/ask",
        json={"question": "What is the weather today?"}
    )

    assert response.status_code == 200
    assert response.json()["question_type"] == "unsupported"


def test_empty_question():
    response = client.post(
        "/ask",
        json={"question": ""}
    )

    assert response.status_code == 400


def test_compare_months(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "interpret_question",
        lambda question: {
            "intent": "compare_months",
            "month1": "2026-05",
            "month2": "2026-06"
        }
    )

    response = client.post(
        "/ask",
        json={"question": "Compare May 2026 and June 2026"}
    )

    print("\nACTUAL API RESPONSE:")
    print(response.json())

    assert response.status_code == 200
