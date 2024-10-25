import requests
import pytest

BASE_URL = "http://localhost:4000/api/food/list"
IMAGE_FILE_PATH = "/home/amogh/Pictures/Wallpapers/leaves.png"


def add_food(name, description, price, category, image_file):
    """Helper function to add food."""
    with open(image_file, 'rb') as f:
        files = {'image': f}
        response = requests.post("http://localhost:4000/api/food/add", data={
            "name": name,
            "description": description,
            "price": price,
            "category": category
        }, files=files)
    return response


def list_food():
    """Helper function to retrieve food list."""
    response = requests.get(BASE_URL)
    return response


@pytest.fixture(scope="module")
def setup():
    """Set up for test cases: Create some food items if necessary."""

    add_food("Pizza", "Delicious cheese pizza",
             9.99, "Main Course", IMAGE_FILE_PATH)
    add_food("Burger", "Cheese burger", 5.99, "Main Course", IMAGE_FILE_PATH)

    yield


def test_successful_food_listing(setup):
    """Test case for successfully listing all food items."""
    response = list_food()
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
