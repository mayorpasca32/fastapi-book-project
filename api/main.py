from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.router import api_router

# Initialize FastAPI app
app = FastAPI()

# Middleware should be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router with a prefix
app.include_router(api_router, prefix=settings.API_PREFIX)

# Define individual routes
@app.get("/books/")
def get_books():
    """Returns a list of books."""
    return [{"id": 1, "title": "Book Title"}]

@app.get("/healthcheck")
async def health_check():
    """Checks if the server is active."""
    return {"status": "active"}
