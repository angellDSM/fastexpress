"""Pruebas de integración de la API REST."""
import pytest

from backend.app import app


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_api_ok(client):
    r = client.post("/api/cotizar", json={"peso": 10, "tipo_cliente": "VIP", "tipo_envio": "EXPRESS"})
    assert r.status_code == 200 and r.get_json()["total"] == 47.25


def test_api_peso_no_numerico(client):
    r = client.post("/api/cotizar", json={"peso": "abc", "tipo_cliente": "VIP", "tipo_envio": "EXPRESS"})
    assert r.status_code == 400


def test_api_peso_ausente(client):
    r = client.post("/api/cotizar", json={})
    assert r.status_code == 400


def test_frontend_se_sirve(client):
    r = client.get("/")
    assert r.status_code == 200 and b"FastExpress" in r.data


def test_api_limite_excedido(client):
    r = client.post("/api/cotizar", json={"peso": 20.01, "tipo_cliente": "NUEVO", "tipo_envio": "ESTANDAR"})
    assert r.status_code == 422
