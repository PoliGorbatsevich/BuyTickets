import datetime
from typing import TypeVar, Generic
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


T = TypeVar("T")


class BaseTicketSchema(BaseModel):
    place_number: int
    row_number: int
    price: int


class CreateTicketSchema(BaseTicketSchema):
    pass


class UpdateTicketSchema(BaseTicketSchema):
    pass


class TicketSchema(BaseTicketSchema):
    id: int
    owner_id: int | None
    performance_id: int

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
