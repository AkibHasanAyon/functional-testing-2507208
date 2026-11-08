"""Functional tests for the Flask web application (app.py)."""

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """GET / should return 200 and contain the title."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Functional Testing Dashboard" in response.data


def test_health_endpoint(client):
    """GET /health should return JSON with a sha field."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert "sha" in data


@pytest.mark.parametrize("func_name, args, expected_result", [
    ("is_adult", {"age": "20"}, True),
    ("is_adult", {"age": "15"}, False),
    ("celsius_to_fahrenheit", {"celsius": "100"}, 212.0),
    ("count_vowels", {"text": "hello"}, 2),
    ("invert", {"flag": "true"}, False),
    ("greet", {"name": "World"}, "Hello, World!"),
    ("greet", {"name": ""}, "Hello, Guest!"),
    ("find_max", {"numbers": "[1, 5, 3]"}, 5),
    ("get_price", {"prices": '{"apple": 1.5}', "item": "apple"}, 1.5),
    ("swap", {"pair": "[1, 2]"}, [2, 1]),
    ("is_leap_year", {"year": "2024"}, True),
    ("to_int", {"value": "42"}, 42),
    ("divide", {"a": "10", "b": "2"}, 5.0),
    ("power", {"base": "2", "exponent": "3"}, 8.0),
    ("square_root", {"x": "16"}, 4.0),
    ("factorial", {"n": "5"}, 120),
    ("average", {"numbers": "[2, 4, 6]"}, 4.0),
])
def test_run_success(client, func_name, args, expected_result):
    """POST /run with valid inputs should return correct result."""
    response = client.post("/run", json={"function": func_name, "args": args})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == expected_result


def test_run_common_items(client):
    """common_items returns a set converted to list."""
    response = client.post("/run", json={
        "function": "common_items",
        "args": {"set_a": "[1, 2, 3]", "set_b": "[2, 3, 4]"}
    })
    assert response.status_code == 200
    data = response.get_json()
    assert sorted(data["result"]) == [2, 3]


@pytest.mark.parametrize("func_name, args, expected_error_type", [
    ("is_adult", {"age": "-5"}, "ValueError"),
    ("count_vowels", {"text": 123}, "TypeError"),
    ("find_max", {"numbers": "[]"}, "ValueError"),
    ("divide", {"a": "10", "b": "0"}, "ZeroDivisionError"),
    ("square_root", {"x": "-1"}, "ValueError"),
    ("factorial", {"n": "-1"}, "ValueError"),
    ("unknown_func", {}, "ValueError"),
])
def test_run_errors(client, func_name, args, expected_error_type):
    """POST /run with invalid inputs should return 400 and error info."""
    response = client.post("/run", json={"function": func_name, "args": args})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["type"] == expected_error_type
