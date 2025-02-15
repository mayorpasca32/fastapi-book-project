import sys
import os
from fastapi.testclient import TestClient  # Import FastAPI's test client
from main import app  # Import the FastAPI app

# Ensure the correct module path is set
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create the test client
client = TestClient(app)


# Test fetching all books
def test_get_all_books():
    response = client.get("/api/v1/books/")  # Updated path
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure response is a list


# Test fetching a single book
def test_get_single_book():
    response = client.get("/api/v1/books/1")  # Updated path
    assert response.status_code == 200
    data = response.json()

    assert "title" in data
    assert "author" in data


# Test creating a book
def test_create_book():
    new_book = {
        "id": 4,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "publication_year": 1997,
        "genre": "Fantasy",
    }
    response = client.post("/api/v1/books/", json=new_book)  # Updated path
    assert response.status_code == 201
    data = response.json()

    assert data["id"] == 4
    assert data["title"] == "Harry Potter and the Sorcerer's Stone"


# Test updating a book
def test_update_book():
    updated_book = {
        "id": 1,
        "title": "The Hobbit: An Unexpected Journey",
        "author": "J.R.R. Tolkien",
        "publication_year": 1937,
        "genre": "Fantasy",
    }
    response = client.put("/api/v1/books/1", json=updated_book)  # Updated path
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "The Hobbit: An Unexpected Journey"


# Test deleting a book
def test_delete_book():
    response = client.delete("/api/v1/books/3")  # Updated path
    assert response.status_code == 204  # No content

    # Check that the book no longer exists
    response = client.get("/api/v1/books/3")
    assert response.status_code == 404  # Not found
