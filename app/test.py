import time
from unittest.mock import ANY

from fastapi.testclient import TestClient

from .main import app, get_error, get_latency, set_latency, set_error

client = TestClient(app)


def test_index() -> None:
    response = client.get("/producer")
    assert response.status_code == 200
    assert response.json() == {"secret": ANY, "ts": ANY}


def test_index_with_latency() -> None:
    set_latency(0.51)
    s = time.time()
    response = client.get("/producer")
    e = time.time()

    assert e - s > 0.5
    assert response.status_code == 200
    assert response.json() == {"secret": ANY, "ts": ANY}


def test_index_with_error() -> None:
    set_error(400)
    response = client.get("/producer")
    assert response.status_code == 400


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == ""


def test_set_latency() -> None:
    response = client.get("/producer/inject/latency?value=0.45")
    assert response.status_code == 200
    assert response.json() == ""
    assert get_latency() == 0.45


def test_set_error() -> None:
    response = client.get("/producer/inject/error?code=400")
    assert response.status_code == 200
    assert response.json() == ""
    assert get_error() == 400
