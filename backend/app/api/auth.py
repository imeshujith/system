from fastapi import APIRouter, HTTPException, status
import jwt

from app.application.auth import create_access_token, create_refresh_token, verify_password, get_password_hash
from app.schemas.auth import Token, TokenData, LoginRequest
from datetime import timedelta
from app.config import settings
from app.domain.auth import DatabaseService
from app.schemas.auth import TokenRefreshRequest
from app.schemas.user import UserCreate

router = APIRouter(prefix="/api/v1")

# Register a new user
@router.post("/signup", response_model=Token)
async def register(user_data: UserCreate):
    if DatabaseService().get_user_by_username(user_data.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if DatabaseService().get_user_by_email(user_data.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = get_password_hash(user_data.password)
    DatabaseService().create_user(user_data.username, user_data.email, hashed_password)

    # Generate both access and refresh tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.username, "email": user_data.email},
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": user_data.username, "email": user_data.email},
        expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Login a user and generate both access and refresh tokens
@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    user = DatabaseService().get_user_by_username(login_request.username)

    if user is None or not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate both access and refresh tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "email": user.email},
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": user.username, "email": user.email},
        expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# Update the refresh token route
@router.post("/refresh-token", response_model=Token)
async def refresh_token(request: TokenRefreshRequest):
    refresh_token = request.refresh_token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"Authorization": "Bearer"},
    )

    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        email: str = payload.get("email")
        if username is None or email is None:
            raise credentials_exception
        token_data = TokenData(username=username, email=email)
    except jwt.PyJWTError:
        raise credentials_exception

    user = DatabaseService().get_user_by_username(token_data.username)
    if user is None or user.email != token_data.email:
        raise credentials_exception

    # Generate a new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}