from fastapi import HTTPException
from sqlalchemy.orm import Session

from BuyTickets.models.ticket import Ticket, Performance
from BuyTickets.schemas.ticket import TicketSchema, CreateTicketSchema, UpdateTicketSchema


class TicketService:
    # @staticmethod
    # def get_tickets(db: Session, skip: int = 0, limit: int = 100) -> list[Ticket]:
    #     return db.query(Ticket).offset(skip).limit(limit).all()

    @staticmethod
    def _get_ticket_by_id(db: Session, ticket_id: int) -> Ticket:
        ret = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if ret is None:
            raise HTTPException(status_code=404, detail="We dont find such ticket")
        return ret

    @staticmethod
    def _get_tickets_by_performance_id(db: Session, performance_id: int) -> list[Ticket]:
        ret = db.query(Ticket).filter(Ticket.performance_id == performance_id).all()
        if ret is None:
            raise HTTPException(status_code=404, detail="We dont find such ticket")
        return ret

    def get_tickets_by_performance_id(self, db: Session, performance_id: int) -> list[Ticket]:
        return self._get_tickets_by_performance_id(db=db, performance_id=performance_id)

    def get_ticket_by_id(self, db: Session, ticket_id: int) -> Ticket:
        return self._get_ticket_by_id(db=db, ticket_id=ticket_id)

    def create_ticket(self, db: Session, performance_id: int, place_number: int, row_number: int, price: int) -> Ticket:
        _ticket = Ticket(place_number=place_number,
                         row_number=row_number,
                         price=price,
                         performance_id=performance_id)
        if db.query(Performance).filter(Performance.id == performance_id).first() is None:
            raise HTTPException(status_code=404, detail="We dont find such Performance")
        db.add(_ticket)
        db.commit()
        db.refresh(_ticket)
        return _ticket

    def create_all_tickets(self, db: Session, performance_id: int, row_length: int, row_count: int, price: int):
        row = 1
        while row <= row_count:
            place = 1
            while place <= row_length:
                self.create_ticket(db=db,
                                   performance_id=performance_id,
                                   place_number=place,
                                   row_number=row,
                                   price=price)
                place += 1
            row += 1

    def remove_ticket(self, db: Session, ticket_id: int):
        _ticket = self._get_ticket_by_id(db=db, ticket_id=ticket_id)
        db.delete(_ticket)
        db.commit()

    def update_ticket(self, db: Session, ticket_id: int, ticket: UpdateTicketSchema) -> Ticket:
        _ticket = self._get_ticket_by_id(db=db, ticket_id=ticket_id)
        _ticket.price = ticket.price
        _ticket.row_number = ticket.row_number
        _ticket.place_number = ticket.place_number
        db.commit()
        db.refresh(_ticket)
        return _ticket
