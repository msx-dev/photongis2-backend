from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

test_user = {"email": "test@test.com", "password": "Justtesting123"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == "All good."


def test_signup_success():
    response = client.post("/auth/signup", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_signup_existing_email():
    response = client.post("/auth/signup", json=test_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success():
    response = client.post("/auth/login", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_credentials():
    response = client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_refresh_token_success():
    login_response = client.post("/auth/login", json=test_user)
    refresh_token = login_response.json()["refresh_token"]

    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_token_invalid():
    response = client.post("/auth/refresh", json={"refresh_token": "invalidtoken"})
    assert response.status_code == 401
