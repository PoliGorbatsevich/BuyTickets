from fastapi import APIRouter, Depends

from BuyTickets.schemas.ticket import CreateTicketSchema, Response, UpdateTicketSchema
from BuyTickets.database import get_session
from sqlalchemy.orm import Session
from BuyTickets.services.ticket_service import TicketService

router = APIRouter(prefix='/ticket')


@router.post(path='/create')
async def create_ticket(request: CreateTicketSchema,
                        service: TicketService = Depends(),
                        db: Session = Depends(get_session)):
    service.create_ticket(db=db, ticket=request)
    return Response(code=200,
                    status='Ok',
                    message='Ticket created successfully').dict(exclude_none=True)


@router.get(path='/')
async def get_tickets(service: TicketService = Depends(),
                      db: Session = Depends(get_session)):
    _ticket = service.get_ticket(db=db, skip=0, limit=100)
    return Response(code=200,
                    status='Ok',
                    message='Success Fetch all data',
                    result=_ticket).dict(exclude_none=True)


@router.get(path='/{ticket_id}')
async def get_ticket_by_id(ticket_id: int,
                           service: TicketService = Depends(),
                           db: Session = Depends(get_session)):
    _ticket = service.get_ticket_by_id(db=db, ticket_id=ticket_id)
    return Response(code=200,
                    status='Ok',
                    message='Success get data',
                    result=_ticket).dict(exclude_none=True)


@router.post(path='/update/{ticket_id}')
async def update_ticket(ticket_id: int,
                        request: UpdateTicketSchema,
                        service: TicketService = Depends(),
                        db: Session = Depends(get_session)):
    _ticket = service.update_ticket(db=db, ticket_id=ticket_id, ticket=request)
    return Response(code=200,
                    status='Ok',
                    message='Success update data',
                    result=_ticket).dict(exclude_none=True)


@router.delete(path='/{delete}')
async def delete_ticket(ticket_id: int,
                        service: TicketService = Depends(),
                        db: Session = Depends(get_session)):
    service.remove_ticket(db=db, ticket_id=ticket_id)
    return Response(code=200,
                    status='Ok',
                    message='Success delete data').dict(exclude_none=True)

