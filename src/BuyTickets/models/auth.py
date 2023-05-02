import datetime

from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, Time, DateTime
from sqlalchemy.orm import relationship, validates
from starlette import status

from BuyTickets.enums import Role, PaymentAccess, PaymentType
from BuyTickets.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    is_active = Column(Boolean, default=True)
    username = Column(String)
    email = Column(String, unique=True)
    role = Column(Enum(Role), default=Role.USER)
    hashed_password = Column(String)
    balance = Column(Integer, default=0)

    tickets = relationship("Ticket", back_populates="owner")
    transactions = relationship("Transaction", back_populates="user")

    @validates("email")
    def validate_email(self, key, address):
        if "@" not in address:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Почта введена некорректно")
        return address


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, index=True, unique=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    payment = Column(Integer, default=0)
    payment_type = Column(Enum(PaymentType))
    description = Column(String)
    access = Column(Enum(PaymentAccess))
    datetime = Column(DateTime, default=datetime.datetime.now())

    user = relationship("User", back_populates="transactions")
