import pytest
from fastapi.testclient import TestClient

from app import data
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def restaurar_datos():
    """Cada test empieza con los datos originales (el POST modifica la lista)."""
    copia = [dict(u) for u in data.USERS]
    yield
    data.USERS[:] = copia


def test_v1_devuelve_nombre():
    r = client.get("/v1/users")
    assert r.status_code == 200
    assert r.json()[0] == {"id": 1, "nombre": "Eva"}


def test_v2_devuelve_fullname_y_email():
    r = client.get("/v2/users")
    assert r.status_code == 200
    assert r.json()[0] == {"id": 1, "fullName": "Eva", "email": "eva@example.com"}


def test_v1_avisa_de_deprecacion():
    r = client.get("/v1/users")
    assert r.headers["Deprecation"] == "@1790812800"
    assert "Sunset" in r.headers
    assert "successor-version" in r.headers["Link"]


def test_v2_no_tiene_cabeceras_de_deprecacion():
    r = client.get("/v2/users")
    assert "Deprecation" not in r.headers
    assert "Sunset" not in r.headers


def test_usuario_inexistente_da_404_en_ambas_versiones():
    assert client.get("/v1/users/999").status_code == 404
    assert client.get("/v2/users/999").status_code == 404


def test_crear_usuario_en_v2_devuelve_201():
    r = client.post("/v2/users", json={"fullName": "Marie", "email": "marie@example.com"})
    assert r.status_code == 201
    assert r.json()["fullName"] == "Marie"
    # y la v1 también lo ve (mismos datos, distinto contrato)
    nombres = [u["nombre"] for u in client.get("/v1/users").json()]
    assert "Marie" in nombres


def test_post_en_v1_no_existe():
    r = client.post("/v1/users", json={"nombre": "X"})
    assert r.status_code == 405  # la ruta existe pero no admite POST
