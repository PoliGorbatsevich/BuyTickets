from fastapi import APIRouter, Depends

from BuyTickets.schemas.ticket import CreateTicketSchema, Response, UpdateTicketSchema
from BuyTickets.database import get_session
from sqlalchemy.orm import Session
from BuyTickets.services.ticket_service import TicketService
from BuyTickets.services.auth_service import auth_permission, admin_manager_permission, admin_permission

router = APIRouter(prefix='/ticket')


@router.post(path='/create', dependencies=[Depends(admin_manager_permission)])
async def create_ticket(performance_id: int,
                        place_number: int,
                        row_number: int,
                        price: int,
                        service: TicketService = Depends(),
                        db: Session = Depends(get_session)):
    _ticket = service.create_ticket(db=db,
                                    performance_id=performance_id,
                                    place_number=place_number,
                                    row_number=row_number,
                                    price=price)
    print(_ticket)
    return Response(code=200,
                    status='Ok',
                    message='Ticket created successfully',
                    result=_ticket).dict(exclude_none=True)


# @router.get(path='/')
# async def get_tickets(service: TicketService = Depends(),
#                       db: Session = Depends(get_session)):
#     _ticket = service.get_tickets(db=db, skip=0, limit=100)
#     return Response(code=200,
#                     status='Ok',
#                     message='Success Fetch all data',
#                     result=_ticket).dict(exclude_none=True)


@router.get(path='/{ticket_id}', dependencies=[Depends(auth_permission)])
async def get_ticket_by_id(ticket_id: int,
                           service: TicketService = Depends(),
                           db: Session = Depends(get_session)):
    _ticket = service.get_ticket_by_id(db=db, ticket_id=ticket_id)
    return Response(code=200,
                    status='Ok',
                    message='Success get data',
                    result=_ticket).dict(exclude_none=True)


@router.post(path='/{ticket_id}/update', dependencies=[Depends(admin_manager_permission)])
async def update_ticket(ticket_id: int,
                        request: UpdateTicketSchema,
                        service: TicketService = Depends(),
                        db: Session = Depends(get_session)):
    _ticket = service.update_ticket(db=db, ticket_id=ticket_id, ticket=request)
    return Response(code=200,
                    status='Ok',
                    message='Success update data',
                    result=_ticket).dict(exclude_none=True)


@router.delete(path='/{ticket_id}', dependencies=[Depends(admin_manager_permission)])
async def delete_ticket(ticket_id: int,
                        service: TicketService = Depends(),
                        db: Session = Depends(get_session)):
    service.remove_ticket(db=db, ticket_id=ticket_id)
    return Response(code=200,
                    status='Ok',
                    message='Success delete data').dict(exclude_none=True)
