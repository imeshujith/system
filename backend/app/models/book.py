import uuid

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.domain.db import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publication_date = Column(Date, nullable=True)
    isbn = Column(String, unique=True, nullable=True)
    cover_image = Column(String, nullable=True)

    # User association
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="books")

    # Metadata fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

