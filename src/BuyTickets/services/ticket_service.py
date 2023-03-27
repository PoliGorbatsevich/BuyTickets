from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from BuyTickets.models.ticket import Ticket, Performance
from BuyTickets.schemas.ticket import TicketSchema, CreateTicketSchema, UpdateTicketSchema
from BuyTickets.database import get_session


class TicketService:
    def __init__(self, session: Session = Depends(get_session)):
        self.db = session

    def _get_ticket_by_id(self, ticket_id: int) -> Ticket:
        ret = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if ret is None:
            raise HTTPException(status_code=404, detail="We dont find such ticket")
        return ret

    def _get_tickets_by_performance_id(self, performance_id: int) -> list[Ticket]:
        ret = self.db.query(Ticket).filter(Ticket.performance_id == performance_id).all()
        if ret is None:
            raise HTTPException(status_code=404, detail="We dont find such ticket")
        return ret

    def get_tickets_by_performance_id(self, performance_id: int) -> list[Ticket]:
        return self._get_tickets_by_performance_id(performance_id=performance_id)

    def get_ticket_by_id(self, ticket_id: int) -> Ticket:
        return self._get_ticket_by_id(ticket_id=ticket_id)

    def _get_ticket_by_performance_id(self, ticket_id: int, performance_id: int) -> Ticket:
        ret = self.db.query(Ticket).filter(Ticket.id == ticket_id,
                                           Ticket.performance_id == performance_id).first()
        if ret is None:
            raise HTTPException(status_code=404, detail="We dont find such ticket")
        return ret

    def get_ticket_by_performance_id(self, ticket_id: int, performance_id: int) -> Ticket:
        return self._get_ticket_by_performance_id(ticket_id=ticket_id, performance_id=performance_id)

    def create_ticket(self, ticket: CreateTicketSchema, performance_id: int) -> Ticket:
        if self.db.query(Performance).filter(Performance.id == performance_id).first() is None:
            raise HTTPException(status_code=404, detail="We dont find such Performance")
        if self.db.query(Ticket).filter(Ticket.place_number == ticket.place_number,
                                        Ticket.performance_id == performance_id,
                                        Ticket.row_number == ticket.row_number).first():
            raise HTTPException(status_code=404, detail="This ticket exists")
        _ticket = Ticket(place_number=ticket.place_number,
                         row_number=ticket.row_number,
                         price=ticket.price,
                         performance_id=performance_id)
        self.db.add(_ticket)
        self.db.commit()
        self.db.refresh(_ticket)
        return _ticket

    def create_all_tickets(self, performance_id: int, row_length: int, row_count: int, price: int):
        row = 1
        while row <= row_count:
            place = 1
            while place <= row_length:
                _ticket = CreateTicketSchema(place_number=place,
                                             row_number=row,
                                             price=price)
                self.create_ticket(_ticket, performance_id=performance_id,)
                place += 1
            row += 1

    def remove_ticket(self, ticket_id: int):
        _ticket = self._get_ticket_by_id(ticket_id=ticket_id)
        self.db.delete(_ticket)
        self.db.commit()

    def update_ticket(self, ticket_id: int, ticket: UpdateTicketSchema) -> Ticket:
        _ticket = self._get_ticket_by_id(ticket_id=ticket_id)
        _ticket.price = ticket.price
        _ticket.row_number = ticket.row_number
        _ticket.place_number = ticket.place_number
        self.db.commit()
        self.db.refresh(_ticket)
        return _ticket

    def buy_ticket(self, ticket: Ticket, user_id: int):
        if ticket.owner_id:
            raise HTTPException(status_code=404, detail="This ticket is already bought")
        ticket.owner_id = user_id
        ticket.owner.balance -= ticket.price
        self.db.commit()
        self.db.refresh(ticket)
        self.db.refresh(ticket.owner)
        return ticket

    def return_ticket(self, ticket: Ticket, index: float):
        ticket.owner.balance += ticket.price * index
        self.db.commit()
        self.db.refresh(ticket.owner)

        ticket.owner_id = None
        self.db.commit()
        self.db.refresh(ticket)
        return ticket





