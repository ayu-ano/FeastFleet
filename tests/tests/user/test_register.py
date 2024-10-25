import requests
import pytest

BASE_URL = "http://localhost:4000/api/user/register"


def create_user(email, name, password):
    """Helper function to register a user."""
    response = requests.post(BASE_URL, json={
        "email": email,
        "name": name,
        "password": password
    })
    return response


@pytest.fixture(scope="module")
def setup():
    """Set up for test cases: create initial user for testing."""
    # Create an initial user to test against
    create_user("testuser@example.com", "Test User", "SecurePassword123")
    yield


def test_successful_registration(setup):
    """Test case for successful user registration."""
    response = create_user("successfuluser@example.com",
                           "Successful User", "Password123")
    assert response.status_code == 200
    assert response.json()["success"] == True


def test_missing_email(setup):
    """Test case for missing email."""
    response = create_user("", "No Email User", "Password123")
    assert response.status_code == 200
    assert response.json() == {"success": False,
                               "message": "Please enter a valid email."}


def test_missing_username(setup):
    """Test case for missing username."""
    response = create_user("nousername@example.com", "", "Password123")
    assert response.status_code == 200
    assert response.json() == {"success": False,
                               "message": "Error"}


def test_missing_password(setup):
    """Test case for missing password."""
    response = create_user("nopassword@example.com", "No Password User", "")
    assert response.status_code == 200
    assert response.json() == {"success": False,
                               "message": "Please enter a strong password."}


def test_email_already_exists(setup):
    """Test case for email already exists."""
    response = create_user("testuser@example.com",
                           "Duplicate Email User", "Password123")
    assert response.status_code == 200
    assert response.json() == {"success": False,
                               "message": "User already exists."}


def test_invalid_email_format(setup):
    """Test case for invalid email format."""
    response = create_user(
        "invalid-email", "Invalid Email User", "Password123")
    assert response.status_code == 200
    assert response.json() == {"success": False,
                               "message": "Please enter a valid email."}


def test_short_password(setup):
    """Test case for short password."""
    response = create_user("shortpwd@example.com",
                           "Short Password User", "short")
    assert response.status_code == 200
    assert response.json() == {
        "success": False, "message": "Please enter a strong password."}


def test_successful_registration_with_existing_email(setup):
    """Test case for attempting to register with an existing email."""
    response = create_user("successfuluser@example.com",
                           "Another User", "AnotherPassword123")
    assert response.status_code == 200
    assert response.json() == {"success": False,
                               "message": "User already exists."}
