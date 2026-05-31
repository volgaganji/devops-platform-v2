import os
import sys

sys.path.append(os.path.abspath("backend"))

from app import app, init_db


def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_home():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Real-Time DevOps" in response.data


def test_get_products():
    init_db()

    client = app.test_client()
    response = client.get("/products")

    assert response.status_code == 200