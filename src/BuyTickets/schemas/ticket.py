import datetime
from typing import TypeVar, Generic
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


T = TypeVar("T")

# class Ticket(Base):
#     __tablename__ = "ticket"
#
#     id = Column(Integer, primary_key=True, index=True, unique=True)
#     price = Column(Integer, )
#     place_number = Column(Integer, )
#     row_number = Column(Integer, )
#
#     performance_id = Column(Integer, ForeignKey("performance.id"))
#
#
# class Performance(Base):
#     __tablename__ = "performance"
#
#     id = Column(Integer, primary_key=True, index=True, unique=True)
#     name = Column(String, )
#     description = Column(String, )
#     date = Column(Date, )
#     time = Column(Time, )
#
#     tickets = relationship("ticket")


class BaseTicketSchema(BaseModel):
    place_number: int
    row_number: int
    price: int
    performance_id: int


class CreateTicketSchema(BaseTicketSchema):
    pass


class UpdateTicketSchema(BaseTicketSchema):
    pass


class TicketSchema(BaseTicketSchema):
    id: int
    owner_id: int | None

    class Config:
        orm_mode = True


class BasePerformanceSchema(BaseModel):
    name: str | None
    description: str | None
    date: datetime.date | None
    time: datetime.time | None


class CreatePerformanceSchema(BasePerformanceSchema):
    pass


class UpdatePerformanceSchema(BasePerformanceSchema):
    pass


class PerformanceSchema(BasePerformanceSchema):
    id: int | None
    tickets: list[TicketSchema] = []

    class Config:
        orm_mode = True


class RequestTicket(BaseModel):
    parameter: TicketSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: T | None
