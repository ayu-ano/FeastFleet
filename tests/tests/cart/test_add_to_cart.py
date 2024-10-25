import requests
import pytest

LOGIN_URL = "http://localhost:4000/api/user/login"
ADD_TO_CART_URL = "http://localhost:4000/api/cart/add"

USER_EMAIL = "amogh@g.com"  # Replace with valid email
USER_NAME = "Amogh"  # Replace with valid name
USER_PASSWORD = "abcdefghij"  # Replace with valid password


def add_user(email, name, password):
    """Helper function to create a new user."""
    response = requests.post("http://localhost:4000/api/user/register", json={
        "email": email,
        "name": name,
        "password": password
    })
    return response


def add_to_cart(token, item_id):
    """Helper function to add item to cart using the token."""
    headers = {"token": token}
    response = requests.post(ADD_TO_CART_URL, json={
        "itemId": item_id
    }, headers=headers)
    return response


ITEM_ID = '671b051a754b979a02c506d7'
user_token = add_user(USER_EMAIL, USER_NAME, USER_PASSWORD).json().get("token")


@pytest.fixture(scope="module")
def setup():
    yield
    # Cleanup code if necessary (e.g., remove added items from the cart)
    requests.delete('http://localhost:4000/api/user/deleteAll')


def test_successful_addition_to_cart(setup):
    """Test case for successfully adding a new item to the cart using token."""
    response = add_to_cart(user_token, ITEM_ID)
    assert response.status_code == 200  # Assuming 200 OK for success
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Added to cart"


def test_adding_existing_item_to_cart(setup):
    """Test case for adding an existing item to increase its quantity."""
    # First add the item to cart
    add_to_cart(user_token, ITEM_ID)

    # Add the same item again
    response = add_to_cart(user_token, ITEM_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Added to cart"


def test_invalid_token():
    """Test case for invalid token usage."""
    fake_token = "invalid.token.value"
    response = add_to_cart(fake_token, ITEM_ID)

    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Error"


def test_nonexistent_item(setup):
    """Test case for trying to add a non-existent item to the cart."""
    fake_item_id = "626262626262626262626262"  # Fake item ID
    response = add_to_cart(user_token, fake_item_id)

    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Added to cart"
