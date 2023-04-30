import datetime
import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from BuyTickets.settings import settings
from BuyTickets.models import ticket, auth
from BuyTickets.models.ticket import Performance
from BuyTickets.services.performance_service import PerformanceService
from BuyTickets.schemas.ticket import CreatePerformanceSchema, UpdatePerformanceSchema
from schemas.auth import UserRegistrationSchema
from services.auth_service import AuthService

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


def test_create_performance():
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


def test_get_performance_by_id():
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


def test_get_performance_by_date():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    _performance = service.create_performance(performance)
    assert performance.date == _performance.date
    with pytest.raises(HTTPException):
        service.get_performance_by_date(datetime.date.today() - datetime.timedelta(days=100))
    session.close()


def test_remove_performance():
    performance = CreatePerformanceSchema(name='Test Performance',
                                          description='This is a test performance',
                                          date=datetime.date.today() + datetime.timedelta(days=1),
                                          time=datetime.time(hour=18, minute=0))
    session = Session()
    service = PerformanceService(session=session)
    _performance = service.create_performance(performance=performance)
    with pytest.raises(HTTPException):
        service.remove_performance(_performance.id + 1)
    service.remove_performance(_performance.id)
    session.close()
    with pytest.raises(HTTPException):
        service.get_performance_by_id(_performance.id)


def test_update_performance():
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


def test_actual_performances():
    session = Session()
    service = PerformanceService(session=session)
    performances = service.get_actual_performances()
    for performance in performances:
        assert performance.date >= datetime.date.today()
    session.close()


def test_create_user():
    strr = str(datetime.datetime.now().microsecond)
    user = UserRegistrationSchema(email=strr+"@gmail.com",
                                  username=strr,
                                  password='1111')
    session = Session()
    service = AuthService(session=session)
    with pytest.raises(HTTPException):
        assert service.create_user(user)
    user = UserRegistrationSchema(email=strr+"@gmail.com",
                                  username=strr,
                                  password='111111')
    _user = service.create_user(user)
    assert _user.email == user.email
    assert _user.username == user.username
    assert _user.hashed_password != user.password
    with pytest.raises(HTTPException):
        service.create_user(user)
    session.close()
