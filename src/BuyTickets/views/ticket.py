from fastapi import APIRouter, HTTPException, Path, Depends

from BuyTickets.schemas import RequestTicket, CreateTicketSchema, Response, UpdateTicketSchema
from BuyTickets.database import get_session
from sqlalchemy.orm import Session
from BuyTickets.services import ticket_service

router = APIRouter(prefix='/ticket')


@router.post(path='/create')
async def create_ticket(request: CreateTicketSchema, db: Session = Depends(get_session)):
    ticket_service.create_ticket(db=db, ticket=request)
    return Response(code=200,
                    status='Ok',
                    message='Ticket created successfully').dict(exclude_none=True)


@router.get(path='/')
async def get_tickets(db: Session = Depends(get_session)):
    _ticket = ticket_service.get_ticket(db=db, skip=0, limit=100)
    return Response(code=200,
                    status='Ok',
                    message='Success Fetch all data',
                    result=_ticket).dict(exclude_none=True)


@router.get(path='/{ticket_id}')
async def get_ticket_by_id(ticket_id: int, db: Session = Depends(get_session)):
    _ticket = ticket_service.get_ticket_by_id(db=db, ticket_id=ticket_id)
    return Response(code=200,
                    status='Ok',
                    message='Success get data',
                    result=_ticket).dict(exclude_none=True)


@router.post(path='/update/{ticket_id}')
async def update_ticket(ticket_id: int, request: UpdateTicketSchema, db: Session = Depends(get_session)):
    _ticket = ticket_service.update_ticket(db=db, ticket_id=ticket_id, ticket=request)
    return Response(code=200,
                    status='Ok',
                    message='Success update data',
                    result=_ticket).dict(exclude_none=True)


@router.delete(path='/{delete}')
async def delete_ticket(ticket_id: int, db: Session = Depends(get_session)):
    ticket_service.remove_ticket(db=db, ticket_id=ticket_id)
    return Response(code=200,
                    status='Ok',
                    message='Success delete data').dict(exclude_none=True)

