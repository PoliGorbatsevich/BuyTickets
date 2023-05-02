from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from BuyTickets.schemas.auth import UserSchema, TokenSchema, UserRegistrationSchema
from BuyTickets.services.auth_service import AuthService
from BuyTickets.settings import settings

router = APIRouter(prefix='/auth', tags=["authentication"])


@router.post('/registration', response_model=UserSchema)
def create_user(user_data: UserRegistrationSchema,
                service: AuthService = Depends()):
    return service.create_user(user_data)


@router.post("/token", response_model=TokenSchema)
def get_token(form_data: OAuth2PasswordRequestForm = Depends(),
              service: AuthService = Depends()):
    return service.get_access_token(username=form_data.username,
                                    password=form_data.password)


@router.get("/users/me/", response_model=UserSchema)
def read_users_me(service: AuthService = Depends(),
                  token: str = Depends(settings.oauth2_scheme)):
    return service.get_current_active_user(token)
