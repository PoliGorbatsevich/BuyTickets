from datetime import timedelta, datetime

from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session


from BuyTickets.database import get_session
from BuyTickets.models.auth import User, Transaction
from BuyTickets.settings import settings
from BuyTickets.schemas.auth import UserRegistrationSchema, TokenDataSchema
from BuyTickets.enums import Role, PaymentType, PaymentAccess

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_user(self, username: str) -> User:
        user = (self.session.query(User)
                .filter(User.username == username)
                .first())
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого пользователя не существует")
        return user

    def get_user(self, username: str) -> User:
        return self._get_user(username=username)

    def authenticate_user(self, username: str,
                          password: str, ) -> User:
        user = self._get_user(username=username)
        if not self._verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неправильный пароль",
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
            raise HTTPException(status_code=400, detail="Пользователь был удален")
        return current_user

    def get_access_token(self, username: str, password: str) -> dict:
        user = self.authenticate_user(username=username, password=password)
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = self._create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token,
                "token_type": "bearer",
                "role": user.role.value}

    def create_user(self, user_data: UserRegistrationSchema) -> User:
        if len(user_data.password) < 6:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Пароль должен быть больше 6 символов")
        operation = (self.session.query(User)
                     .filter(User.username == user_data.username)
                     .first())
        if operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Пользователь с таким логином уже зарегистрирован")
        operation = (self.session.query(User)
                     .filter(User.email == user_data.email)
                     .first())
        if operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Пользователь с такой почтой уже зарегистрирован")

        user = User(username=user_data.username,
                    email=user_data.email,
                    hashed_password=self._get_password_hash(user_data.password))
        self.session.add(user)
        self.session.commit()
        return user

    def change_password(self, token: str, old_pass: str, new_pass: str, new_pass1: str):
        _user = self.get_current_active_user(token=token)
        if not self._verify_password(old_pass, _user.hashed_password):
            raise HTTPException(status_code=404, detail="Старый пароль не совпадет")
        if len(new_pass) < 6:
            raise HTTPException(status_code=404, detail="Пароль должен быть больше 6 символов")
        if new_pass != new_pass1:
            raise HTTPException(status_code=404, detail="Новые пароли не совпадают")
        _user.hashed_password = self._get_password_hash(new_pass)

        self.session.commit()
        self.session.refresh(_user)
        return _user

    def get_tickets(self, token: str):
        _user = self.get_current_active_user(token=token)
        return _user.tickets

    def top_up_balance(self, token: str, payment: int):
        _user = self.get_current_active_user(token=token)
        if payment <= 0:
            self.session.add(Transaction(user_id=_user.id,
                                         payment=payment,
                                         description='Failed to top up the balance, got wrong integer.',
                                         access=PaymentAccess.REJECTED,
                                         payment_type=PaymentType.PLUS))
            self.session.commit()
            raise HTTPException(status_code=400, detail="Нельзя пополнить баланс на сумму меньше 0")
        self.session.add(Transaction(user_id=_user.id,
                                     access=PaymentAccess.CONFIRMED,
                                     payment=payment,
                                     payment_type=PaymentType.PLUS,
                                     description='Top up balance.'))
        _user.balance += payment
        self.session.commit()
        self.session.refresh(_user)
        return _user

    def transaction_history(self, token: str) -> list:
        user_id = self.get_current_active_user(token=token).id
        return self.session.query(Transaction).filter(Transaction.user_id == user_id).all()


class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, token: str = Depends(settings.oauth2_scheme), service: AuthService = Depends()):
        user = service.get_current_active_user(token=token)
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")


admin_permission = RoleChecker([Role.ADMIN])
manager_permission = RoleChecker([Role.MANAGER])
admin_manager_permission = RoleChecker([Role.MANAGER, Role.ADMIN])
auth_permission = RoleChecker([Role.USER, Role.ADMIN, Role.MANAGER])
