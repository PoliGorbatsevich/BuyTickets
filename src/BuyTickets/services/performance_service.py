from fastapi import HTTPException
from sqlalchemy.orm import Session

from BuyTickets.models.ticket import Performance
from BuyTickets.schemas.ticket import CreatePerformanceSchema, UpdatePerformanceSchema


class PerformanceService:
    # @staticmethod
    # def get_performance(db: Session, skip: int = 0, limit: int = 100) -> list[Performance]:
    #     return db.query(Performance).offset(skip).limit(limit).all()

    @staticmethod
    def _get_performance_by_id(db: Session, performance_id: int):
        ret = db.query(Performance).filter(Performance.id == performance_id).first()
        if ret is None:
            raise HTTPException(status_code=404, detail="We dont find such performance")
        return ret

    def get_performance_by_id(self, db: Session, performance_id: int) -> Performance:
        return self._get_performance_by_id(db=db, performance_id=performance_id)

    @staticmethod
    def create_performance(db: Session, performance: CreatePerformanceSchema) -> Performance:
        _performance = Performance(name=performance.name,
                                   description=performance.description,
                                   date=performance.date,
                                   time=performance.time)
        db.add(_performance)
        db.commit()
        db.refresh(_performance)
        return _performance

    def get_all_tickets(self, db: Session, performance_id: int) -> list:
        ret = self._get_performance_by_id(db=db, performance_id=performance_id)
        return ret.tickets

    def remove_performance(self, db: Session, performance_id: int):
        _performance = self._get_performance_by_id(db=db, performance_id=performance_id)
        db.delete(_performance)
        db.commit()

    def update_performance(self, db: Session, performance_id: int, performance: UpdatePerformanceSchema) -> Performance:
        _performance = self._get_performance_by_id(db=db, performance_id=performance_id)
        _performance.name = performance.name
        _performance.date = performance.date
        _performance.time = performance.time
        db.commit()
        db.refresh(_performance)
        return _performance
