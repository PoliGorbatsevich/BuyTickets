from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from BuyTickets.enums import Role
from BuyTickets.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    is_active = Column(Boolean, default=True)
    username = Column(String)
    email = Column(String)
    role = Column(Enum(Role), default=Role.USER)
    hashed_password = Column(String)
    balance = Column(Integer, default=0)

    tickets = relationship("Ticket", back_populates="owner")
