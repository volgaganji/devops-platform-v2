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
def test_create_product():
    init_db()

    client = app.test_client()
    response = client.post(
        "/products",
        json={"name": "Test Product", "price": 999},
    )

    assert response.status_code == 201
    assert response.get_json()["message"] == "product added"
def test_update_product():
    init_db()

    client = app.test_client()

    create_response = client.post(
        "/products",
        json={"name": "Old Product", "price": 100},
    )

    product_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/products/{product_id}",
        json={"name": "Updated Product", "price": 200},
    )

    assert update_response.status_code == 200
    assert update_response.get_json()["message"] == "product updated"