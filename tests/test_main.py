"""
Tests for the Soko Bora price-tracking API.
Uses an in-memory SQLite database so tests never touch a real database.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest  # noqa: E402
from app.main import create_app, db  # noqa: E402


@pytest.fixture
def client():
    app = create_app(test_config={
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
    })
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_health_route(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_create_price_entry(client):
    payload = {
        "crop_name": "Maize",
        "market_name": "Kimironko Market",
        "region": "Kigali",
        "price_per_kg": 350,
        "currency": "RWF",
        "reported_by": "farmer_jane",
    }
    response = client.post("/api/prices", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["crop_name"] == "Maize"
    assert data["price_per_kg"] == 350
    assert "id" in data


def test_create_price_entry_missing_fields(client):
    response = client.post("/api/prices", json={"crop_name": "Maize"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_list_prices(client):
    client.post("/api/prices", json={
        "crop_name": "Beans",
        "market_name": "Nyabugogo Market",
        "region": "Kigali",
        "price_per_kg": 800,
    })
    client.post("/api/prices", json={
        "crop_name": "Maize",
        "market_name": "Musanze Market",
        "region": "Musanze",
        "price_per_kg": 300,
    })

    response = client.get("/api/prices")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_list_prices_filtered_by_region(client):
    client.post("/api/prices", json={
        "crop_name": "Beans",
        "market_name": "Nyabugogo Market",
        "region": "Kigali",
        "price_per_kg": 800,
    })
    client.post("/api/prices", json={
        "crop_name": "Maize",
        "market_name": "Musanze Market",
        "region": "Musanze",
        "price_per_kg": 300,
    })

    response = client.get("/api/prices?region=Kigali")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["region"] == "Kigali"
