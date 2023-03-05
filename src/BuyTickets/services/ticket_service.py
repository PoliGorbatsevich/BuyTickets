from sqlalchemy.orm import Session

from BuyTickets.models.ticket import Ticket
from BuyTickets.schemas.ticket import TicketSchema, CreateTicketSchema, UpdateTicketSchema


class TicketService:
    @staticmethod
    def get_ticket(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Ticket).offset(skip).limit(100).all()

    @staticmethod
    def _get_ticket_by_id(db: Session, ticket_id: int):
        return db.query(Ticket).filter(Ticket.id == ticket_id).first()

    def get_ticket_by_id(self, db: Session, ticket_id: int):
        return self._get_ticket_by_id(db=db, ticket_id=ticket_id)

    def create_ticket(self, db: Session, ticket: CreateTicketSchema):
        _ticket = Ticket(performance=ticket.performance,
                         description=ticket.description,
                         price=ticket.price)
        db.add(_ticket)
        db.commit()
        db.refresh(_ticket)
        return _ticket

    def remove_ticket(self, db: Session, ticket_id: int):
        _ticket = self._get_ticket_by_id(db=db, ticket_id=ticket_id)
        db.delete(_ticket)
        db.commit()

    def update_ticket(self, db: Session, ticket_id: id, ticket: UpdateTicketSchema):
        _ticket = self._get_ticket_by_id(db=db, ticket_id=ticket_id)
        _ticket.price = ticket.price
        _ticket.description = ticket.description
        _ticket.performance = ticket.performance
        db.commit()
        db.refresh(_ticket)
        return _ticket
