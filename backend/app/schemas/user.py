from pydantic import BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=20)

    @validator("username")
    def validate_username(cls, username):
        if not username.isalnum():
            raise ValueError("Username must contain only alphanumeric characters or underscores.")
        return username

    @validator("password")
    def validate_password(cls, password):
        if len(password) < 6 or len(password) > 20:
            raise ValueError("Password must be between 6 and 20 characters.")
        return password