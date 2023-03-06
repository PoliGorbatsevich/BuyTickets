from sqlalchemy import Integer, String, Column, Time, Date, ForeignKey
from sqlalchemy.orm import relationship

from BuyTickets.database import Base


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    price = Column(Integer, )
    place_number = Column(Integer, )
    row_number = Column(Integer, )
    performance_id = Column(Integer, ForeignKey("performance.id"))
    owner_id = Column(Integer, ForeignKey('user.id'))

    performance = relationship("Performance", back_populates="tickets")
    owner = relationship("User", back_populates="tickets")


class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, )
    description = Column(String, )
    date = Column(Date, )
    time = Column(Time, )

    tickets = relationship("Ticket", back_populates="performance")
