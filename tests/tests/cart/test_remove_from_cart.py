import requests
import pytest

LOGIN_URL = "http://localhost:4000/api/user/login"
REMOVE_FROM_CART_URL = "http://localhost:4000/api/cart/remove"

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


def remove_from_cart(token, item_id):
    """Helper function to remove an item from cart using the token."""
    headers = {"token": token}
    response = requests.post(REMOVE_FROM_CART_URL, json={
        "itemId": item_id
    }, headers=headers)
    return response


@pytest.fixture(scope="module")
def setup():
    yield
    # Cleanup code if necessary (e.g., remove added items from the cart)
    requests.delete('http://localhost:4000/api/user/deleteAll')


# def test_successful_removal_from_cart(setup):
#     """Test case for successfully removing an item from the cart."""
#     response = remove_from_cart(user_token, ITEM_ID)
#     data = response.json()
#     assert data["success"] is True
#     assert data["message"] == "Removed from cart"


def test_removal_of_nonexistent_item(setup):
    """Test case for removing an item that is not in the cart."""
    fake_item_id = "626262626262626262626262"  # Fake item ID
    response = remove_from_cart(user_token, fake_item_id)

    # This depends on how you handle non-existent items
    # Assuming it still returns 200 but with a different message
    data = response.json()
    # Assuming success is False when item doesn't exist
    assert data["success"] is False
    assert data["message"] == "Not Authorized Login Again"


# def test_remove_item_with_zero_quantity(setup):
#     """Test case for trying to remove an item that already has 0 quantity."""
#     # First, remove the item until its quantity reaches 0
#     for _ in range(2):  # Adjust the number depending on initial item quantity
#         remove_from_cart(user_token, ITEM_ID)

#     # Now try to remove the item again when it's already at 0
#     response = remove_from_cart(user_token, ITEM_ID)

#     data = response.json()
#     assert data["success"] is True  # Assuming it still returns success
#     assert data["message"] == "Removed from cart"


def test_invalid_token():
    """Test case for invalid token usage."""
    fake_token = "invalid.token.value"
    response = remove_from_cart(fake_token, ITEM_ID)

    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Error"
