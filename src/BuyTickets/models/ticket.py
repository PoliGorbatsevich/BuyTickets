from sqlalchemy import Integer, String, Column
from BuyTickets.database import Base


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True)
    performance = Column(String, )
    description = Column(String, )
    price = Column(Integer, )
