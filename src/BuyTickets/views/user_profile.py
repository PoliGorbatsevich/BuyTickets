import datetime

from fastapi import APIRouter, Depends, HTTPException

from BuyTickets.services.auth_service import AuthService
from BuyTickets.settings import settings
from BuyTickets.services.auth_service import auth_permission, admin_manager_permission, admin_permission
from BuyTickets.services.ticket_service import TicketService

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
    print(old_pass, new_pass, new_pass1)
    return service.change_password(token=token,
                                   old_pass=old_pass,
                                   new_pass=new_pass,
                                   new_pass1=new_pass1)


@router.get(path='/my_tickets', dependencies=[Depends(auth_permission)])
def my_tickets(service: AuthService = Depends(),
               token: str = Depends(settings.oauth2_scheme)):
    return service.get_tickets(token=token)


@router.post(path='/top_up_balance', dependencies=[Depends(auth_permission)])
def top_up_balance(payment: int,
                   service: AuthService = Depends(),
                   token: str = Depends(settings.oauth2_scheme)):
    return service.top_up_balance(token=token, payment=payment)


@router.post(path='/my_tickets/{ticket_id}/return_ticket', dependencies=[Depends(auth_permission)])
def return_ticket(ticket_id: int,
                  service: AuthService = Depends(),
                  token: str = Depends(settings.oauth2_scheme),
                  ticket_service: TicketService = Depends()):
    user = service.get_current_active_user(token)
    ticket = ticket_service.get_ticket_by_id(ticket_id=ticket_id)
    return ticket_service.return_ticket(ticket=ticket, user=user)


@router.get('/transaction_history/', response_model=list, dependencies=[Depends(auth_permission)])
def transaction_history(service: AuthService = Depends(),
                        token: str = Depends(settings.oauth2_scheme)):
    return service.transaction_history(token=token)

