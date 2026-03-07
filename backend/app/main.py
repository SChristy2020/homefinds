from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, products, orders, waiting_list, reservations, room

app = FastAPI(title="HomeFinds API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router,       prefix="/api/users",        tags=["Users"])
app.include_router(products.router,    prefix="/api/products",     tags=["Products"])
app.include_router(orders.router,      prefix="/api/orders",       tags=["Orders"])
app.include_router(waiting_list.router,prefix="/api/waiting-list", tags=["Waiting List"])
app.include_router(reservations.router,prefix="/api/reservations", tags=["Reservations"])
app.include_router(room.router,        prefix="/api/room",         tags=["Room"])

@app.get("/")
def root():
    return {"message": "HomeFinds API is running"}
