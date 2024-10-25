import requests
import pytest

BASE_URL = "http://localhost:4000/api/food/add"
IMAGE_FILE_PATH = "/home/amogh/Pictures/Wallpapers/leaves.png"


def add_food(name, description, price, category, image_file):
    """Helper function to add food."""
    with open(image_file, 'rb') as f:
        files = {'image': f}
        response = requests.post(BASE_URL, data={
            "name": name,
            "description": description,
            "price": price,
            "category": category
        }, files=files)
    return response


@pytest.fixture(scope="module")
def setup():
    """Set up for test cases."""
    yield


def test_successful_food_addition(setup):
    """Test case for successful food addition."""
    response = add_food("Pizza", "Delicious cheese pizza",
                        9.99, "Main Course", IMAGE_FILE_PATH)
    assert response.json()["success"] == True


def test_missing_name(setup):
    """Test case for missing food name."""
    response = add_food("", "Tasty burger", 5.99,
                        "Main Course", IMAGE_FILE_PATH)
    assert response.json() == {"success": False, "message": "Error"}


def test_missing_description(setup):
    """Test case for missing food description."""
    response = add_food("Burger", "", 5.99, "Main Course", IMAGE_FILE_PATH)
    assert response.json() == {"success": False, "message": "Error"}


def test_missing_price(setup):
    """Test case for missing food price."""
    response = add_food("Sushi", "Delicious sushi", "",
                        "Main Course", IMAGE_FILE_PATH)
    assert response.json() == {"success": False, "message": "Error"}


def test_missing_category(setup):
    """Test case for missing food category."""
    response = add_food("Pasta", "Creamy pasta", 8.99, "", IMAGE_FILE_PATH)
    assert response.json() == {"success": False, "message": "Error"}
