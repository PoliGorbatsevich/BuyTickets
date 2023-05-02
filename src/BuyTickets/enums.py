from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class PaymentAccess(Enum):
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


class PaymentType(Enum):
    PLUS = "plus"
    MINUS = "minus"

