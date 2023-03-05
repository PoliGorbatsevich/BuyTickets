from typing import TypeVar, Generic
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


T = TypeVar("T")


class BaseTicketSchema(BaseModel):
    performance: str | None
    description: str | None
    price: int | None


class CreateTicketSchema(BaseTicketSchema):
    pass


class UpdateTicketSchema(BaseTicketSchema):
    pass


class TicketSchema(BaseTicketSchema):
    id: int | None

    class Config:
        orm_mode = True


class RequestTicket(BaseModel):
    parameter: TicketSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: T | None





