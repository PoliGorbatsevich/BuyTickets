from datetime import timedelta, datetime

from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from BuyTickets.database import get_session
from BuyTickets.models.auth import User
from BuyTickets.settings import settings
from BuyTickets.schemas.auth import UserRegistrationSchema, TokenDataSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_user(self, username: str) -> User:
        user = (self.session.query(User)
                .filter_by(username=username)
                .first())
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    def get_user(self, username: str) -> User:
        return self._get_user(username=username)

    def authenticate_user(self, username: str,
                          password: str, ) -> User:
        user = self._get_user(username=username)
        if not self._verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def _get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def _create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    def get_current_user(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenDataSchema(username=username)
        except JWTError:
            raise credentials_exception
        user = self._get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    def get_current_active_user(self, token: str) -> User:
        current_user = self.get_current_user(token)
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    def get_access_token(self, username: str, password: str) -> dict:
        user = self.authenticate_user(username=username, password=password)
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = self._create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def create_user(self, user_data: UserRegistrationSchema) -> User:
        operation = (self.session.query(User)
                     .filter_by(username=user_data.username)
                     .first())
        if operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        operation = (self.session.query(User)
                     .filter_by(email=user_data.email)
                     .first())
        if operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        user_data.hashed_password = self._get_password_hash(user_data.hashed_password)
        user = User(**user_data.dict())
        self.session.add(user)
        self.session.commit()
        return user
