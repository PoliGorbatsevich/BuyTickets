import uvicorn
from fastapi import FastAPI

from BuyTickets.models import ticket
from BuyTickets.views.ticket import router as ticket_router
from BuyTickets.database import engine

ticket.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(ticket_router)


if __name__ == '__main__':
    uvicorn.run(app)
