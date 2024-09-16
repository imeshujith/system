from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.domain.db import init_db
from app.api.auth import router as auth_routes
from app.api.book import router as book_routes
from app.config import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes)
app.include_router(book_routes)


# Startup event to create tables when the app starts
@app.on_event("startup")
def on_startup():
    init_db()
    logger.info(f"Database connected: {settings.DATABASE_URL}")
    logger.info("Database tables checked/created.")
