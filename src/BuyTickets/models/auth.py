from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref

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

    tickets = relationship("Ticket", back_populates="owner")
