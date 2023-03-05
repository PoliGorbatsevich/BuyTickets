from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    email: str
    username: str
    hashed_password: str
    is_active: bool


class UserSchema(UserBaseSchema):
    id: int

    class Config:
        orm_mode = True


class UserRegistrationSchema(UserBaseSchema):
    pass


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None
