import requests


API_URL = "http://127.0.0.1:8000/api/assistant/chat"


def test_recipe_chat():
    response = requests.post(
        API_URL,
        json={
            "message": "Tengo pollo y arroz, ¿qué puedo preparar?"
        },
        timeout=120,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "RECIPE"
    assert "Arroz con pollo" in data["answer"]


def test_substitution_chat():
    response = requests.post(
        API_URL,
        json={
            "message": "¿Con qué puedo sustituir la leche?"
        },
        timeout=120,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "SUBSTITUTION"
    assert "leche de soya" in data["answer"]


def test_question_chat():
    response = requests.post(
        API_URL,
        json={
            "message": "¿Cuánto tiempo debo cocinar el arroz?"
        },
        timeout=120,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "QUESTION"
    assert "15 y 20 minutos" in data["answer"]


def test_recommendation_chat():
    response = requests.post(
        API_URL,
        json={
            "message": "Quiero una cena rápida y saludable."
        },
        timeout=120,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "RECOMMENDATION"
    assert "Ensalada de pollo rápida" in data["answer"]