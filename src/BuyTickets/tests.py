import datetime
import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from BuyTickets.settings import settings
from BuyTickets.models import ticket, auth
from BuyTickets.models.ticket import Performance
from BuyTickets.services.performance_service import PerformanceService
from BuyTickets.schemas.ticket import CreatePerformanceSchema, UpdatePerformanceSchema, CreateTicketSchema, \
    UpdateTicketSchema
from schemas.auth import UserRegistrationSchema
from BuyTickets.services.auth_service import AuthService
from BuyTickets.services.ticket_service import TicketService

engine = create_engine(settings.test_database_url)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

ticket.Base.metadata.create_all(bind=engine)
auth.Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()


def test_create_performance_success():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    _performance = service.create_performance(performance=performance)
    session.close()
    assert isinstance(_performance, Performance)
    assert _performance.date == performance.date
    assert _performance.time == performance.time
    assert _performance.description == performance.description
    assert _performance.name == performance.name
    assert _performance.id > 0


def test_create_performance_fail():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() - datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    with pytest.raises(HTTPException):
        _performance = service.create_performance(performance=performance)
    session.close()


def test_get_performance_by_id_success():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    _performance = service.create_performance(performance)
    _performance = service.get_performance_by_id(performance_id=_performance.id)
    session.close()
    assert isinstance(_performance, Performance)
    assert _performance.date == performance.date
    assert _performance.time == performance.time
    assert _performance.description == performance.description
    assert _performance.name == performance.name
    assert _performance.id > 0


def test_get_performance_by_id_fail():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    _performance = service.create_performance(performance)
    with pytest.raises(HTTPException):
        _performance = service.get_performance_by_id(performance_id=_performance.id + 1)
    session.close()


def test_get_performance_by_date_success():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    _performance = service.create_performance(performance)
    assert performance.date == _performance.date
    session.close()


def test_get_performance_by_date_fail():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    _performance = service.create_performance(performance)
    with pytest.raises(HTTPException):
        service.get_performance_by_date(datetime.date.today() - datetime.timedelta(days=1))
    session.close()


def test_remove_performance_success():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    _performance = service.create_performance(performance=performance)
    service.remove_performance(_performance.id)
    with pytest.raises(HTTPException):
        service.get_performance_by_id(_performance.id)
    session.close()


def test_remove_performance_fail():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    _performance = service.create_performance(performance=performance)
    with pytest.raises(HTTPException):
        service.remove_performance(_performance.id + 1)
    session.close()


def test_update_performance_success():
    update_performance = UpdatePerformanceSchema(name='1111',
                                                 description='1111',
                                                 date=datetime.date.today() + datetime.timedelta(days=2),
                                                 time=datetime.time(hour=19, minute=0))
    performance = CreatePerformanceSchema(name='1',
                                          description='1',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    _performance = service.create_performance(performance=performance)
    _update_performance = service.update_performance(_performance.id, update_performance)
    session.close()
    assert update_performance.name == _update_performance.name
    assert update_performance.description == _update_performance.description
    assert update_performance.date == _update_performance.date
    assert update_performance.time == _update_performance.time


def test_update_performance_fail():
    update_performance = UpdatePerformanceSchema(name='1111',
                                                 description='1111',
                                                 date=datetime.date.today() - datetime.timedelta(days=2),
                                                 time=datetime.time(hour=19, minute=0))
    performance = CreatePerformanceSchema(name='1',
                                          description='1',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    _performance = service.create_performance(performance=performance)
    with pytest.raises(HTTPException):
        _update_performance = service.update_performance(_performance.id, update_performance)
    session.close()


def test_actual_performances():
    session = Session()
    service = PerformanceService(session=session)
    performances = service.get_actual_performances()
    for performance in performances:
        assert performance.date >= datetime.date.today()
    session.close()


def test_create_user_success():
    strr = str(datetime.datetime.now().microsecond)

    session = Session()
    service = AuthService(session=session)
    user = UserRegistrationSchema(email=strr + "@gmail.com",
                                  username=strr,
                                  password='111111')
    _user = service.create_user(user)
    assert _user.email == user.email
    assert _user.username == user.username
    assert _user.hashed_password != user.password
    with pytest.raises(HTTPException):
        service.create_user(user)
    session.close()


def test_create_user_fail():
    strr = str(datetime.datetime.now().microsecond)
    user = UserRegistrationSchema(email=strr + "@gmail.com",
                                  username=strr,
                                  password='1111')
    session = Session()
    service = AuthService(session=session)
    with pytest.raises(HTTPException):
        assert service.create_user(user)
    session.close()


def test_create_ticket_success():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))

    ticket = CreateTicketSchema(place_number=1,
                                row_number=1,
                                price=1)

    session = Session()
    performance_service = PerformanceService(session=session)
    _performance = performance_service.create_performance(performance=performance)

    session = Session()
    ticket_service = TicketService(session)
    _ticket = ticket_service.create_ticket(ticket=ticket, performance_id=_performance.id)
    session.close()
    assert _ticket.row_number == ticket.row_number
    assert _ticket.place_number == ticket.place_number
    assert _ticket.price == ticket.price


def test_create_ticket_fail():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))

    ticket = CreateTicketSchema(place_number=1,
                                row_number=1,
                                price=1)

    session = Session()
    performance_service = PerformanceService(session=session)
    _performance = performance_service.create_performance(performance=performance)

    session = Session()
    ticket_service = TicketService(session)
    with pytest.raises(HTTPException):
        _ticket = ticket_service.create_ticket(ticket=ticket, performance_id=_performance.id + 1)
    _ticket = ticket_service.create_ticket(ticket=ticket, performance_id=_performance.id)
    with pytest.raises(HTTPException):
        _ticket = ticket_service.create_ticket(ticket=ticket, performance_id=_performance.id)
    session.close()


def test_update_ticket_success():
    ticket = CreateTicketSchema(place_number=1,
                                row_number=1,
                                price=1)
    update_ticket = UpdateTicketSchema(place_number=1,
                                       row_number=1,
                                       price=1)

    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))


    session = Session()
    performance_service = PerformanceService(session=session)
    _performance = performance_service.create_performance(performance=performance)
    service = TicketService(session=session)
    _ticket = service.create_ticket(ticket=ticket, performance_id=_performance.id)
    _update_ticket = service.update_ticket(_ticket.id, update_ticket)
    session.close()
    assert _update_ticket.price == update_ticket.price
    assert _update_ticket.place_number == update_ticket.place_number
    assert _update_ticket.row_number == update_ticket.row_number


def test_update_ticket_fail():
    ticket = CreateTicketSchema(place_number=1,
                                row_number=1,
                                price=1)
    update_ticket = UpdateTicketSchema(place_number=1,
                                       row_number=1,
                                       price=1)

    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))

    session = Session()
    performance_service = PerformanceService(session=session)
    _performance = performance_service.create_performance(performance=performance)
    service = TicketService(session=session)
    _ticket = service.create_ticket(ticket=ticket, performance_id=_performance.id)
    with pytest.raises(HTTPException):
        _update_ticket = service.update_ticket(_ticket.id+1, update_ticket)
    session.close()


def test_remove_ticket_success():
    ticket = CreateTicketSchema(place_number=1,
                                row_number=1,
                                price=1)

    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))

    session = Session()
    performance_service = PerformanceService(session=session)
    _performance = performance_service.create_performance(performance=performance)
    service = TicketService(session=session)
    _ticket = service.create_ticket(ticket=ticket, performance_id=_performance.id)
    service.remove_ticket(ticket_id=_ticket.id)
    with pytest.raises(HTTPException):
        _update_ticket = service.get_ticket_by_id(_ticket.id)
    session.close()


def test_remove_ticket_fail():
    ticket = CreateTicketSchema(place_number=1,
                                row_number=1,
                                price=1)

    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))

    session = Session()
    performance_service = PerformanceService(session=session)
    _performance = performance_service.create_performance(performance=performance)
    service = TicketService(session=session)
    _ticket = service.create_ticket(ticket=ticket, performance_id=_performance.id)
    with pytest.raises(HTTPException):
        service.remove_ticket(ticket_id=_ticket.id+1)
    session.close()
