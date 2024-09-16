import logging

from app.domain.book import BookService

logger = logging.getLogger(__name__)

# Initialize the BookService
def get_book_service() -> BookService:
    return BookService()

def add_book(user_id: int, title: str, author: str, publication_date: str = None, isbn: str = None,
             cover_image: str = None):
    book_service = get_book_service()
    try:
        new_book = book_service.add_book(user_id, title, author, publication_date, isbn, cover_image)

        if not new_book["success"]:
            logger.error(new_book["message"])
            return new_book

        logger.info(f"Book added successfully: {new_book[1].title} by {new_book[1].author}")
        return new_book
    except Exception as e:
        logger.error(f"Failed to add book: {e}")
        raise
    finally:
        book_service.db.close()


def get_books(user_id: int, page: int = 1, limit: int = 10):
    book_service = get_book_service()
    try:
        # Retrieve paginated books from the book service
        response = book_service.get_books(user_id, page, limit)

        # Log the details including pagination info
        if response["success"]:
            logger.info(
                f"Retrieved page {page} of books for user {user_id}, total books: {response['pagination']['total']}")
        else:
            logger.warning(f"Failed to retrieve books for user {user_id}: {response.get('message', 'Unknown error')}")

        return response

    except Exception as e:
        logger.error(f"Exception occurred while retrieving books for user {user_id}: {e}")
        raise

    finally:
        book_service.db.close()


def get_book_by_id(book_id: str, user_id: int):
    book_service = get_book_service()
    try:
        book = book_service.get_book_by_id(book_id, user_id)
        if book:
            logger.info(f"Retrieved book: {book.title} by {book.author} for user {user_id}")
        else:
            logger.warning(f"Book with ID {book_id} not found for user {user_id}")
        return book
    except Exception as e:
        logger.error(f"Failed to retrieve book with ID {book_id} for user {user_id}: {e}")
        raise
    finally:
        book_service.db.close()


def update_book_by_id(book_id: str, user_id: int, title: str = None, author: str = None,
                      publication_date: str = None, isbn: str = None, cover_image: str = None):
    book_service = get_book_service()
    try:
        # Attempt to update the book
        updated_book = book_service.update_book(book_id, user_id, title, author, publication_date, isbn, cover_image)

        # Log based on success or failure
        if updated_book["success"]:
            logger.info(f"Successfully updated book ID {book_id}: '{title}' by {author} for user {user_id}")
        else:
            logger.warning(
                f"Failed to update book ID {book_id}: {updated_book.get('message')} for user {user_id}")
        return updated_book

    except Exception as e:
        # Log any exception that occurs
        logger.error(f"Exception occurred while updating book ID {book_id} for user {user_id}: {e}")
        return {"success": False, "message": "An error occurred while updating the book."}

    finally:
        # Close the database session/connection if applicable
        book_service.db.close()


def delete_book_by_id(book_id: str, user_id: int):
    book_service = get_book_service()
    try:
        result = book_service.delete_book(book_id, user_id)
        if result:
            logger.info(f"Book with ID {book_id} soft-deleted for user {user_id}")
        else:
            logger.warning(f"Book with ID {book_id} not found or already deleted for user {user_id}")
        return result
    except Exception as e:
        logger.error(f"Failed to delete book with ID {book_id} for user {user_id}: {e}")
        raise
    finally:
        book_service.db.close()

def search_books(user_id: int, search_query: str):
    book_service = get_book_service()
    try:
        books = book_service.search_books(user_id, search_query)
        logger.info(f"Found {len(books)} books for user {user_id} with search query '{search_query}'")
        return books
    except Exception as e:
        logger.error(f"Failed to search books for user {user_id} with query '{search_query}': {e}")
        raise
    finally:
        book_service.db.close()

def get_library_summary(user_id: int):
    book_service = get_book_service()
    try:
        summary = book_service.get_library_summary(user_id)
        logger.info(f"Library summary for user {user_id}: {summary['total_books']} total books")
        return summary
    except Exception as e:
        logger.error(f"Failed to get library summary for user {user_id}: {e}")
        raise
    finally:
        book_service.db.close()
