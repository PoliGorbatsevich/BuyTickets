import datetime

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from BuyTickets.models.ticket import Performance
from BuyTickets.schemas.ticket import CreatePerformanceSchema, UpdatePerformanceSchema
from BuyTickets.database import get_session


class PerformanceService:
    def __init__(self, session: Session = Depends(get_session)):
        self.db = session
    
    def get_performance_by_date(self, date: datetime.date):
        return self.db.query(Performance).filter(Performance.date == date).all()

    def _get_performance_by_id(self, performance_id: int):
        ret = self.db.query(Performance).filter(Performance.id == performance_id).first()
        if ret is None:
            raise HTTPException(status_code=404, detail="We dont find such performance")
        return ret

    def get_performance_by_id(self, performance_id: int) -> Performance:
        return self._get_performance_by_id(performance_id=performance_id)

    def create_performance(self, performance: CreatePerformanceSchema) -> Performance:
        _performance = Performance(name=performance.name,
                                   description=performance.description,
                                   date=performance.date,
                                   time=performance.time)
        self.db.add(_performance)
        self.db.commit()
        self.db.refresh(_performance)
        return _performance

    def get_all_tickets(self, performance_id: int) -> list:
        ret = self._get_performance_by_id(performance_id=performance_id)
        return ret.tickets

    def remove_performance(self, performance_id: int):
        _performance = self._get_performance_by_id(performance_id=performance_id)
        self.db.delete(_performance)
        self.db.commit()

    def update_performance(self, performance_id: int, performance: UpdatePerformanceSchema) -> Performance:
        _performance = self._get_performance_by_id(performance_id=performance_id)
        _performance.name = performance.name
        _performance.date = performance.date
        _performance.time = performance.time
        self.db.commit()
        self.db.refresh(_performance)
        return _performance
