from typing import List  # ✅ Import List for Python 3.8 compatibility
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from api.db.schemas import Book, Genre, InMemoryDB

router = APIRouter()

# Initialize in-memory database
db = InMemoryDB()
db.books = {
    1: Book(
        id=1, title="The Hobbit", author="J.R.R. Tolkien",
        publication_year=1937, genre=Genre.SCI_FI
    ),
    2: Book(
        id=2, title="The Lord of the Rings", author="J.R.R. Tolkien",
        publication_year=1954, genre=Genre.FANTASY
    ),
    3: Book(
        id=3, title="The Return of the King", author="J.R.R. Tolkien",
        publication_year=1955, genre=Genre.FANTASY
    ),
}

@router.get("/api/v1/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """Retrieve a single book by ID."""
    book = db.books.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/api/v1/books", response_model=List[Book], status_code=status.HTTP_200_OK)  # ✅ Fixed List[Book]
async def get_books():
    """Retrieve all books."""
    return list(db.books.values())

@router.post("/api/v1/books", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book: Book):
    """Create a new book entry."""
    db.add_book(book)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=book.model_dump())

@router.put("/api/v1/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book):
    """Update an existing book by ID."""
    updated_book = db.update_book(book_id, book)
    return JSONResponse(status_code=status.HTTP_200_OK, content=updated_book.model_dump())

@router.delete("/api/v1/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Delete a book by ID."""
    db.delete_book(book_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
