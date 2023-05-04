import datetime

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from BuyTickets.models.ticket import Ticket, Performance
from BuyTickets.schemas.ticket import TicketSchema, CreateTicketSchema, UpdateTicketSchema
from BuyTickets.database import get_session
from BuyTickets.enums import PaymentAccess, PaymentType
from BuyTickets.models.auth import User, Transaction


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
                self.create_ticket(_ticket, performance_id=performance_id, )
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

    def buy_ticket(self, ticket: Ticket, user: User):
        if user.balance < ticket.price:
            self.db.add(Transaction(user_id=user.id,
                                    access=PaymentAccess.REJECTED,
                                    payment=ticket.price,
                                    payment_type=PaymentType.MINUS,
                                    description='Failed to buy ticket. Not enough money.'))
            self.db.commit()
            raise HTTPException(status_code=400, detail="Not enough money")
        if ticket.performance.date < datetime.date.today():
            self.db.add(Transaction(user_id=user.id,
                                    access=PaymentAccess.REJECTED,
                                    payment=ticket.price,
                                    payment_type=PaymentType.MINUS,
                                    description='Failed to buy ticket. The performance has already passed.'))
            self.db.commit()
            raise HTTPException(status_code=400,
                                detail="You cannot buy this ticket. The performance has already passed")
        if ticket.performance.date == datetime.date.today():
            if ticket.performance.time < datetime.time:
                if ticket.performance.date < datetime.date.today():
                    self.db.add(Transaction(user_id=user.id,
                                            access=PaymentAccess.REJECTED,
                                            payment=ticket.price,
                                            payment_type=PaymentType.MINUS,
                                            description='Failed to buy ticket. The performance has already passed.'))
                    self.db.commit()
                raise HTTPException(status_code=400,
                                    detail="You cannot buy this ticket. The performance has already passed")
        if ticket.owner_id:
            if ticket.performance.date < datetime.date.today():
                self.db.add(Transaction(user_id=user.id,
                                        access=PaymentAccess.REJECTED,
                                        payment=ticket.price,
                                        payment_type=PaymentType.MINUS,
                                        description='Failed to buy ticket. This ticket is already bought.'))
                self.db.commit()
            raise HTTPException(status_code=404, detail="This ticket is already bought")

        self.db.add(Transaction(user_id=user.id,
                                access=PaymentAccess.CONFIRMED,
                                payment=ticket.price,
                                payment_type=PaymentType.MINUS,
                                description='Bought a ticket.'))
        ticket.owner_id = user.id
        ticket.owner.balance -= ticket.price
        self.db.commit()
        self.db.refresh(ticket)
        self.db.refresh(ticket.owner)
        return ticket

    def return_ticket(self, ticket: Ticket, user: User):
        index = 1
        if ticket.owner_id != user.id:
            self.db.add(Transaction(user_id=user.id,
                                    payment=ticket.price,
                                    description='Failed to return ticket, You dont have such ticket.',
                                    access=PaymentAccess.REJECTED,
                                    payment_type=PaymentType.PLUS))
            self.db.commit()
            raise HTTPException(status_code=400, detail="You dont have such ticket")
        if ticket.performance.date < datetime.date.today():
            self.db.add(Transaction(user_id=user.id,
                                    payment=ticket.price,
                                    description='Failed to return ticket, the performance has already passed.',
                                    access=PaymentAccess.REJECTED,
                                    payment_type=PaymentType.PLUS))
            self.db.commit()
            raise HTTPException(status_code=400,
                                detail="You cannot return this ticket. The performance has already passed")

        if ticket.performance.date > datetime.date.today():
            index = 1
        elif ticket.performance.date == datetime.date.today():
            if ticket.performance.time > datetime.time:
                index = 0.5
            else:
                self.db.add(Transaction(user_id=user.id,
                                        payment=ticket.price,
                                        description='Failed to return ticket, the performance has already passed.',
                                        access=PaymentAccess.REJECTED,
                                        payment_type=PaymentType.PLUS))
                self.db.commit()
                raise HTTPException(status_code=400,
                                    detail="You cannot return this ticket. The performance has already passed")

        ticket.owner.balance += int(ticket.price * index)
        self.db.commit()
        self.db.refresh(ticket.owner)

        self.db.add(Transaction(user_id=ticket.owner_id,
                                access=PaymentAccess.CONFIRMED,
                                payment=int(ticket.price * index),
                                payment_type=PaymentType.PLUS,
                                description='Ticket returned.'))

        ticket.owner_id = None
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
