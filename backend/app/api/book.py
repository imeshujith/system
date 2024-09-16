from app.application.auth import get_current_user
from app.application.book import add_book, get_books, get_book_by_id, search_books, get_library_summary, \
    update_book_by_id, delete_book_by_id
from app.schemas.book import BookResponse, BookCreate, BookUpdate, LibrarySummary, PaginatedBooksResponse
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List
router = APIRouter(prefix="/api/v1")

@router.post("/books", response_model=BookResponse)
async def create_book(book: BookCreate, user_id: int = Depends(get_current_user)):
    result = add_book(user_id, **book.dict())
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result["data"]


@router.get("/books", response_model=PaginatedBooksResponse)
async def list_books(user_id: int = Depends(get_current_user),
                     page: int = Query(1, ge=1),
                     limit: int = Query(10, le=100)):
    try:
        # Fetch paginated books using the book service
        result = get_books(user_id, page, limit)

        if not result["success"]:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])

        if not result["data"]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found")

        # Optionally include pagination information in the response
        return {
            "books": result["data"],
            "pagination": result.get("pagination", {})
        }

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")


@router.get("/books/{book_id}", response_model=BookResponse)
async def read_book(book_id: str, user_id: int = Depends(get_current_user)):
    try:
        result = get_book_by_id(book_id, user_id)
        if not result["success"]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["message"])
        return result["data"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")

@router.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: str, book_update: BookUpdate, user_id: int = Depends(get_current_user)):
    try:
        result = update_book_by_id(book_id, user_id, **book_update.dict(exclude_unset=True))
        if not result["success"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
        return result["data"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")

@router.delete("/books/{book_id}", response_model=dict)
async def delete_book(book_id: str, user_id: int = Depends(get_current_user)):
    try:
        result = delete_book_by_id(book_id, user_id)
        if not result["success"]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["message"])
        return {"detail": "Book deleted successfully"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")

@router.get("/books/search", response_model=List[BookResponse])
async def search_books_query(search_query: str, user_id: int = Depends(get_current_user)):
    try:
        result = search_books(user_id, search_query)
        if not result["success"]:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
        return result["data"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")

@router.get("/library-summary", response_model=LibrarySummary)
async def library_summary(user_id: int = Depends(get_current_user)):
    try:
        result = get_library_summary(user_id)
        if not result["success"]:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
        return result
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")
