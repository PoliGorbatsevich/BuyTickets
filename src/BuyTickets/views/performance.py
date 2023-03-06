from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from BuyTickets.schemas.ticket import CreatePerformanceSchema, Response, UpdatePerformanceSchema
from BuyTickets.database import get_session
from BuyTickets.services.performance_service import PerformanceService
from BuyTickets.services.auth_service import admin_permission, auth_permission, admin_manager_permission
from BuyTickets.services.ticket_service import TicketService

router = APIRouter(prefix='/performance')


@router.post(path='/create', dependencies=[Depends(admin_manager_permission)])
async def create_performance(row_count: int,
                             row_length: int,
                             price: int,
                             request: CreatePerformanceSchema,
                             service: PerformanceService = Depends(),
                             ticket_service: TicketService = Depends(),
                             db: Session = Depends(get_session)):
    _performance = service.create_performance(db=db, performance=request)
    ticket_service.create_all_tickets(db=db,
                                      performance_id=_performance.id,
                                      row_length=row_length,
                                      row_count=row_count,
                                      price=price)

    return Response(code=200,
                    status='Ok',
                    message='Performance created successfully').dict(exclude_none=True)


@router.get(path='/', dependencies=[Depends(auth_permission)])
async def get_performances(service: PerformanceService = Depends(),
                           db: Session = Depends(get_session)):
    _performance = service.get_performance(db=db, skip=0, limit=100)
    return Response(code=200,
                    status='Ok',
                    message='Success Fetch all data',
                    result=_performance).dict(exclude_none=True)


@router.get(path='/{performance_id}', dependencies=[Depends(auth_permission)])
async def get_performance_by_id(performance_id: int,
                                service: PerformanceService = Depends(),
                                db: Session = Depends(get_session)):
    _performance = service.get_performance_by_id(db=db, performance_id=performance_id)
    return Response(code=200,
                    status='Ok',
                    message='Success get data',
                    result=_performance).dict(exclude_none=True)


@router.post(path='/{performance_id}/update', dependencies=[Depends(admin_manager_permission)])
async def update_performance(performance_id: int,
                             request: UpdatePerformanceSchema,
                             service: PerformanceService = Depends(),
                             db: Session = Depends(get_session)):
    _performance = service.update_performance(db=db, performance_id=performance_id, performance=request)
    return Response(code=200,
                    status='Ok',
                    message='Success update data',
                    result=_performance).dict(exclude_none=True)


@router.delete(path='/{performance_id}/delete', dependencies=[Depends(admin_manager_permission)])
async def delete_performance(performance_id: int,
                             service: PerformanceService = Depends(),
                             db: Session = Depends(get_session)):
    service.remove_performance(db=db, performance_id=performance_id)
    return Response(code=200,
                    status='Ok',
                    message='Success delete data').dict(exclude_none=True)


@router.get(path='/{performance_id}/tickets', dependencies=[Depends(auth_permission)])
async def get_performance_tickets(performance_id: int,
                                  service: PerformanceService = Depends(),
                                  db: Session = Depends(get_session)):
    _tickets = service.get_performance_by_id(db=db, performance_id=performance_id).tickets
    return Response(code=200,
                    status='Ok',
                    message='Success delete data',
                    result=_tickets).dict(exclude_none=True)
