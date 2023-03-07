from fastapi import APIRouter, Depends

from BuyTickets.services.auth_service import AuthService
from BuyTickets.settings import settings
from BuyTickets.services.auth_service import auth_permission, admin_manager_permission, admin_permission

router = APIRouter(prefix='/user_profile', tags=["user_profile"])


@router.get(path='/me', dependencies=[Depends(auth_permission)])
def my_profile(service: AuthService = Depends(),
               token: str = Depends(settings.oauth2_scheme)):
    return service.get_current_active_user(token)


@router.post(path='/change_password', dependencies=[Depends(auth_permission)])
def change_password(service: AuthService = Depends(),
                    token: str = Depends(settings.oauth2_scheme),
                    old_pass: str = None,
                    new_pass: str = None,
                    new_pass1: str = None):
    return service.change_password(token=token,
                                   old_pass=old_pass,
                                   new_pass=new_pass,
                                   new_pass1=new_pass1)


# @router.get(path='/my_tickets', dependencies=[Depends(auth_permission)])
# def my_tickets()