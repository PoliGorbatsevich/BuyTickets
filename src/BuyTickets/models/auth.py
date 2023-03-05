from sqlalchemy import Column, Integer, String, Boolean
from BuyTickets.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
