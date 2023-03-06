import uvicorn
from fastapi import FastAPI

from BuyTickets.models import ticket, auth
from BuyTickets.views.ticket import router as ticket_router
from BuyTickets.views.auth import router as auth_router
from BuyTickets.views.performance import router as performance_router
from BuyTickets.database import engine

ticket.Base.metadata.create_all(bind=engine)
auth.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(ticket_router)
app.include_router(auth_router)
app.include_router(performance_router)


if __name__ == '__main__':
    uvicorn.run(app)
