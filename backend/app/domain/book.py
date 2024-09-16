from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from datetime import datetime

from app.domain.db import SessionLocal
from app.models.book import Book

class BookService:
    def __init__(self):
        self.db: Session = SessionLocal()

    def add_book(self, user_id: int, title: str, author: str, publication_date: str = None, isbn: str = None,
                 cover_image: str = None):
        try:
            # Check if a book with the same ISBN already exists
            if isbn:
                existing_book = self.db.query(Book).filter_by(isbn=isbn).first()
                if existing_book:
                    return {"success": False, "message": "Book with ISBN already exists"}

            # Parse publication date if provided
            if publication_date:
                try:
                    publication_date = datetime.strptime(publication_date, '%Y-%m-%d').date()
                except ValueError:
                    return {"success": False, "message": "Invalid publication date format"}

            new_book = Book(
                title=title,
                author=author,
                publication_date=publication_date,
                isbn=isbn,
                cover_image=cover_image,
                user_id=user_id,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_deleted=False
            )
            self.db.add(new_book)
            self.db.commit()
            self.db.refresh(new_book)
            return {"success": True, "data": new_book}

        except IntegrityError:
            self.db.rollback()
            return {"success": False, "message": "Failed to create new book"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_books(self, user_id: int, page: int = 1, limit: int = 10):
        try:
            # Calculate offset based on the page number and limit
            offset = (page - 1) * limit

            # Query the database with pagination parameters
            books_query = self.db.query(Book).filter(Book.user_id == user_id, Book.is_deleted == False)
            total_books = books_query.count()
            books = books_query.order_by(Book.created_at.desc()).offset(offset).limit(limit).all()

            return {
                "success": True,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total_books,
                    "total_pages": (total_books + limit - 1) // limit  # Calculate total pages
                },
                "data": books
            }
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_book_by_id(self, book_id: str, user_id: int):
        try:
            book = self.db.query(Book).filter(Book.id == book_id, Book.user_id == user_id, Book.is_deleted == False).first()
            if book:
                return {"success": True, "data": book}
            return {"success": False, "message": "Book not found"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def update_book(self, book_id: str, user_id: int, title: str = None, author: str = None,
                    publication_date: str = None,
                    isbn: str = None, cover_image: str = None):
        try:
            # Parse publication date if provided
            if publication_date:
                try:
                    publication_date = datetime.strptime(publication_date, '%Y-%m-%d').date()
                except ValueError:
                    return {"success": False, "message": "Invalid publication date format"}

            book = self.get_book_by_id(book_id, user_id)
            if book["success"]:
                book = book["data"]

                # Check if the new ISBN is already used by another book
                if isbn:
                    existing_book = self.db.query(Book).filter(Book.isbn == isbn, Book.id != book_id).first()
                    if existing_book:
                        return {"success": False, "message": "ISBN already exists for another book"}

                # Update book details
                if title:
                    book.title = title
                if author:
                    book.author = author
                if publication_date:
                    book.publication_date = publication_date
                if isbn:
                    book.isbn = isbn
                if cover_image:
                    book.cover_image = cover_image
                book.updated_at = datetime.now()

                self.db.commit()
                self.db.refresh(book)
                return {"success": True, "data": book}

            return {"success": False, "message": "Book not found"}

        except Exception as e:
            return {"success": False, "message": str(e)}

    def delete_book(self, book_id: str, user_id: int):
        try:
            book = self.get_book_by_id(book_id, user_id)
            if book["success"]:
                book = book["data"]
                book.is_deleted = True
                book.updated_at = datetime.now()
                self.db.commit()
                return {"success": True}
            return {"success": False, "message": "Book not found"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def search_books(self, search_query: str):
        try:
            books = self.db.query(Book).filter(
                or_(
                    Book.title.ilike(f"%{search_query}%"),
                    Book.author.ilike(f"%{search_query}%")
                ),
                Book.is_deleted == False
            ).all()
            return {"success": True, "data": books}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_library_summary(self, user_id: int):
        try:
            total_books = self.db.query(Book).filter(Book.user_id == user_id, Book.is_deleted == False).count()
            recent_additions = self.db.query(Book).filter(Book.user_id == user_id, Book.is_deleted == False).order_by(
                desc(Book.created_at)).limit(5).all()

            return {
                "success": True,
                "total_books": total_books,
                "recent_additions": recent_additions
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
