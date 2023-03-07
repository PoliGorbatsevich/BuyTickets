from fastapi import APIRouter, Depends

from BuyTickets.schemas.ticket import CreateTicketSchema, Response, UpdateTicketSchema
from BuyTickets.services.ticket_service import TicketService
from BuyTickets.services.auth_service import auth_permission, admin_manager_permission, admin_permission, AuthService
from BuyTickets.settings import settings

router = APIRouter(prefix='/performance/{performance_id}/ticket', tags=["ticket"])


@router.post(path='/create', dependencies=[Depends(admin_manager_permission)])
async def create_ticket(performance_id: int,
                        request: CreateTicketSchema,
                        service: TicketService = Depends()):
    _ticket = service.create_ticket(ticket=request, performance_id=performance_id)
    return Response(code=200,
                    status='Ok',
                    message='Ticket created successfully',
                    result=_ticket).dict(exclude_none=True)


@router.get(path='/{ticket_id}', dependencies=[Depends(auth_permission)])
async def get_ticket_by_id(performance_id: int,
                           ticket_id: int,
                           service: TicketService = Depends()):
    _ticket = service.get_ticket_by_performance_id(ticket_id=ticket_id, performance_id=performance_id)
    return Response(code=200,
                    status='Ok',
                    message='Success get data',
                    result=_ticket).dict(exclude_none=True)


@router.post(path='/{ticket_id}/update', dependencies=[Depends(admin_manager_permission)])
async def update_ticket(performance_id: int,
                        ticket_id: int,
                        request: UpdateTicketSchema,
                        service: TicketService = Depends()):
    _ticket = service.update_ticket(ticket_id=ticket_id, ticket=request, performance_id=performance_id)
    return Response(code=200,
                    status='Ok',
                    message='Success update data',
                    result=_ticket).dict(exclude_none=True)


@router.delete(path='/{ticket_id}', dependencies=[Depends(admin_manager_permission)])
async def delete_ticket(performance_id: int,
                        ticket_id: int,
                        service: TicketService = Depends()):
    service.remove_ticket(ticket_id=ticket_id, performance_id=performance_id)
    return Response(code=200,
                    status='Ok',
                    message='Success delete data').dict(exclude_none=True)


@router.post(path='/{ticket_id}/buy', dependencies=[Depends(auth_permission)])
async def buy_ticket(performance_id: int,
                     ticket_id: int,
                     service: TicketService = Depends(),
                     auth: AuthService = Depends(),
                     token: str = Depends(settings.oauth2_scheme)):
    user_id = auth.get_current_active_user(token=token).id
    ticket = service.buy_ticket(ticket_id=ticket_id, user_id=user_id, performance_id=performance_id)
    return Response(code=200,
                    status='Ok',
                    message='Success buy ticket',
                    result=ticket).dict(exclude_none=True)
