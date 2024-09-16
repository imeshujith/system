from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    publication_date: Optional[str] = None
    isbn: Optional[str] = None
    cover_image: Optional[str] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publication_date: Optional[str] = None
    isbn: Optional[str] = None
    cover_image: Optional[str] = None

class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    publication_date: Optional[date] = None
    isbn: Optional[str] = None
    cover_image: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

class Pagination(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int

class PaginatedBooksResponse(BaseModel):
    books: List[BookResponse] = []
    pagination: Pagination = {}


class LibrarySummary(BaseModel):
    total_books: int
    recent_additions: List[BookResponse]