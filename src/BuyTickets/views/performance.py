import datetime

from fastapi import APIRouter, Depends

from BuyTickets.schemas.ticket import CreatePerformanceSchema, Response, UpdatePerformanceSchema
from BuyTickets.services.performance_service import PerformanceService
from BuyTickets.services.auth_service import admin_permission, auth_permission, admin_manager_permission
from BuyTickets.services.ticket_service import TicketService

router = APIRouter(prefix='/performance', tags=["performance"])


@router.post(path='/create', dependencies=[Depends(admin_manager_permission)])
async def create_performance(row_count: int,
                             row_length: int,
                             price: int,
                             request: CreatePerformanceSchema,
                             service: PerformanceService = Depends(),
                             ticket_service: TicketService = Depends()):
    _performance = service.create_performance(performance=request)
    ticket_service.create_all_tickets(performance_id=_performance.id,
                                      row_length=row_length,
                                      row_count=row_count,
                                      price=price)
    print(_performance)
    return _performance.id


@router.get(path='/playbill/', dependencies=[Depends(auth_permission)])
async def get_performances_by_date(date: datetime.date,
                                   service: PerformanceService = Depends()):

    _performance = service.get_performance_by_date(date=date)
    return _performance


@router.get(path='/{performance_id}', dependencies=[Depends(auth_permission)])
async def get_performance_by_id(performance_id: int,
                                service: PerformanceService = Depends()):
    _performance = service.get_performance_by_id(performance_id=performance_id)
    return _performance


@router.post(path='/{performance_id}/update', dependencies=[Depends(admin_manager_permission)])
async def update_performance(performance_id: int,
                             request: UpdatePerformanceSchema,
                             service: PerformanceService = Depends()):
    _performance = service.update_performance(performance_id=performance_id, performance=request)
    return Response(code=200,
                    status='Ok',
                    message='Success update data',
                    result=_performance).dict(exclude_none=True)


@router.delete(path='/{performance_id}/delete', dependencies=[Depends(admin_manager_permission)])
async def delete_performance(performance_id: int,
                             service: PerformanceService = Depends()):
    service.remove_performance(performance_id=performance_id)
    return Response(code=200,
                    status='Ok',
                    message='Success delete data').dict(exclude_none=True)


@router.get(path='/{performance_id}/ticket', dependencies=[Depends(auth_permission)])
async def get_performance_tickets(performance_id: int,
                                  service: PerformanceService = Depends()):
    _tickets = service.get_performance_by_id(performance_id=performance_id).tickets
    return _tickets


@router.get(path='/', response_model=list, dependencies=[Depends(auth_permission)])
async def get_actual_performances(service: PerformanceService = Depends()):
    _performances = service.get_actual_performances()
    return _performances
