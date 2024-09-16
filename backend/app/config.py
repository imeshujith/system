import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    # JWT Secret Keys
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY")

    # JWT Expiration Times
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # Algorithm for JWT
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    # Database URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")


settings = Settings()
