from pydantic import BaseModel

from BuyTickets.enums import Role
from BuyTickets.schemas.ticket import TicketSchema


class UserBaseSchema(BaseModel):
    email: str
    username: str


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool
    hashed_password: str
    role: Role
    tickets: list[TicketSchema] | None
    balance: int

    class Config:
        orm_mode = True


class UserRegistrationSchema(UserBaseSchema):
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    role: str


class TokenDataSchema(BaseModel):
    username: str | None = None
