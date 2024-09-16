from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    email: EmailStr

class TokenRefreshRequest(BaseModel):
    refresh_token: str