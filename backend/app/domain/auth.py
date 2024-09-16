import logging
from datetime import datetime

from sqlalchemy.orm import Session
from app.domain.db import SessionLocal

from app.models.user import User

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.db: Session = SessionLocal()

    def create_user(self, username: str, email: str, hashed_password: str):
        try:
            db_user = User(username=username, email=email, hashed_password=hashed_password, created_at=datetime.now(),
                updated_at=datetime.now())
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            logger.info(f"User {username} created successfully.")
            return db_user
        except Exception as e:
            logger.error(f"Failed to create user {username}: {e}")
            self.db.rollback()
            raise

    def get_user_by_username(self, username: str):
        try:
            user = self.db.query(User).filter(User.username == username).first()
            if user:
                logger.info(f"User {username} found.")
            else:
                logger.warning(f"User {username} not found.")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user {username}: {e}")
            raise

    def get_user_by_email(self, email: str):
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if user:
                logger.info(f"User with email {email} found.")
            else:
                logger.warning(f"User with email {email} not found.")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user with email {email}: {e}")
            raise

    def update_username(self, old_username: str, new_username: str):
        try:
            user = self.db.query(User).filter(User.username == old_username).first()
            if user:
                if self.get_user_by_username(new_username):
                    logger.warning(f"New username {new_username} is already taken.")
                    raise
                user.username = new_username
                self.db.commit()
                logger.info(f"Username updated from {old_username} to {new_username}.")
            else:
                logger.warning(f"User with username {old_username} not found.")
        except Exception as e:
            logger.error(f"Failed to update username from {old_username} to {new_username}: {e}")
            self.db.rollback()
            raise

    def update_password(self, username: str, new_hashed_password: str):
        try:
            user = self.db.query(User).filter(User.username == username).first()
            if user:
                user.hashed_password = new_hashed_password
                self.db.commit()
                logger.info(f"Password updated for user {username}.")
            else:
                logger.warning(f"User with username {username} not found.")
        except Exception as e:
            logger.error(f"Failed to update password for user {username}: {e}")
            self.db.rollback()
            raise
