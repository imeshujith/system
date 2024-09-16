from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from app.config import settings
from app.domain.auth import DatabaseService
from app.schemas.auth import TokenData

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Bearer for access token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Instantiate the database service
auth_db_service = DatabaseService()

# Utility function to hash passwords
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Utility function to verify passwords
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Create access JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Create refresh JWT token
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Get the current user based on token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authorization": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        email: str = payload.get("email")
        if username is None or email is None:
            raise credentials_exception
        token_data = TokenData(username=username, email=email)
    except jwt.PyJWTError:
        raise credentials_exception

    user = auth_db_service.get_user_by_username(token_data.username)
    if user is None or user.email != token_data.email:
        raise credentials_exception
    return user.id