import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from BuyTickets.models import ticket, auth
from BuyTickets.views.ticket import router as ticket_router
from BuyTickets.views.auth import router as auth_router
from BuyTickets.views.performance import router as performance_router
from BuyTickets.views.user_profile import router as user_profile_router
from BuyTickets.database import engine

ticket.Base.metadata.create_all(bind=engine)
auth.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3000/user_profile",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ticket_router)
app.include_router(auth_router)
app.include_router(performance_router)
app.include_router(user_profile_router)


if __name__ == '__main__':
    uvicorn.run(app)
