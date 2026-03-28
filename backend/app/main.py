from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, products, orders, waiting_list, reservations, room, categories, marketing

from pathlib import Path
load_dotenv(Path(__file__).parent.parent / ".env")

app = FastAPI(title="HomeFinds API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router,       prefix="/api/users",        tags=["Users"])
app.include_router(products.router,    prefix="/api/products",     tags=["Products"])
app.include_router(orders.router,      prefix="/api/orders",       tags=["Orders"])
app.include_router(waiting_list.router,prefix="/api/waiting-list", tags=["Waiting List"])
app.include_router(reservations.router,prefix="/api/reservations", tags=["Reservations"])
app.include_router(room.router,        prefix="/api/room",         tags=["Room"])
app.include_router(categories.router,  prefix="/api/categories",   tags=["Categories"])
app.include_router(marketing.router,   prefix="/api/marketing",    tags=["Marketing"])

@app.get("/")
def root():
    return {"message": "HomeFinds API is running"}
