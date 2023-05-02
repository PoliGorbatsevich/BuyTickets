from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = 'postgresql://postgres:postgres@pghost:5432/postgres'
    test_database_url: str = 'postgresql://postgres:postgres@localhost:5432/test_db'
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", )


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
