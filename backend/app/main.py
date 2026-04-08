from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, products, orders, waiting_list, reservations, room, categories, marketing, pickup_settings
from app.database import SessionLocal
from app.services.pickup_reminder_service import send_due_pickup_reminders
import os
import threading
import time

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
app.include_router(marketing.router,        prefix="/api/marketing",         tags=["Marketing"])
app.include_router(pickup_settings.router,  prefix="/api/pickup-settings",   tags=["Pickup Settings"])

def _run_pickup_reminder_scheduler():
    interval = int(os.getenv("PICKUP_REMINDER_INTERVAL_SECONDS", "600"))
    while True:
        db = SessionLocal()
        try:
            result = send_due_pickup_reminders(db)
            if result["sent"] or result["failed"]:
                print(f"[pickup_reminder] {result}")
        except Exception as e:
            print(f"[pickup_reminder] scheduler error: {e}")
        finally:
            db.close()
        time.sleep(interval)

@app.on_event("startup")
def startup_pickup_reminder_scheduler():
    if os.getenv("ENABLE_PICKUP_REMINDER_SCHEDULER", "1") != "1":
        print("[pickup_reminder] scheduler disabled")
        return
    threading.Thread(target=_run_pickup_reminder_scheduler, daemon=True).start()
    print("[pickup_reminder] scheduler started")

@app.get("/")
def root():
    return {"message": "HomeFinds API is running"}
