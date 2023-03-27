from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship, validates
from starlette import status

from BuyTickets.enums import Role
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

    @validates("email")
    def validate_email(self, key, address):
        if "@" not in address:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Почта введена некорректно")
        return address
