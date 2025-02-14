import sys
import os
from fastapi.testclient import TestClient  # Import FastAPI's test client
from api.main import app  # Import the FastAPI app

# Ensure the correct module path is set
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create the test client
client = TestClient(app)


# Ensure the API has a /books/ endpoint (assuming this exists in api.main)
def test_get_all_books():
    response = client.get("/books/")  
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure response is a list


def test_get_single_book():
    response = client.get("/books/1")  
    assert response.status_code == 200
    data = response.json()
    
    assert "title" in data
    assert "author" in data


def test_create_book():
    new_book = {
        "id": 4,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "publication_year": 1997,
        "genre": "Fantasy",
    }
    response = client.post("/books/", json=new_book)  
    assert response.status_code == 201
    data = response.json()
    
    assert data["id"] == 4
    assert data["title"] == "Harry Potter and the Sorcerer's Stone"


def test_update_book():
    updated_book = {
        "id": 1,
        "title": "The Hobbit: An Unexpected Journey",
        "author": "J.R.R. Tolkien",
        "publication_year": 1937,
        "genre": "Fantasy",
    }
    response = client.put("/books/1", json=updated_book)  
    assert response.status_code == 200
    data = response.json()
    
    assert data["title"] == "The Hobbit: An Unexpected Journey"


def test_delete_book():
    response = client.delete("/books/3")  
    assert response.status_code == 204  # No content

    # Check that the book no longer exists
    response = client.get("/books/3")
    assert response.status_code == 404  # Not found
