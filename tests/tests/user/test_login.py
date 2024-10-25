import requests
import pytest

BASE_URL = "http://localhost:4000/api/user/login"


def login_user(email, password):
    """Helper function to log in a user."""
    response = requests.post(BASE_URL, json={
        "email": email,
        "password": password
    })
    return response


@pytest.fixture(scope="module")
def setup():
    """Set up for test cases: create initial user for testing."""
    requests.post("http://localhost:4000/api/user/register", json={
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "SecurePassword123"
    })
    yield
    requests.delete(
        "http://localhost:4000/api/user/deleteAll")


def test_successful_login(setup):
    """Test case for successful user login."""
    response = login_user("testuser@example.com", "SecurePassword123")
    assert response.status_code == 200
    assert response.json()["success"] == True


def test_user_does_not_exist(setup):
    """Test case for user not existing."""
    response = login_user("nonexistentuser@example.com", "SomePassword123")
    assert response.status_code == 200
    assert response.json() == {"success": False,
                               "message": "User doesn't exist."}


def test_invalid_credentials(setup):
    """Test case for invalid credentials (correct email, wrong password)."""
    response = login_user("testuser@example.com", "WrongPassword")
    assert response.status_code == 200
    assert response.json() == {"success": False,
                               "message": "Invalid credentials"}
