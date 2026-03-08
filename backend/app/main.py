import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import users, products, orders, waiting_list, reservations, room, categories

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="HomeFinds API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(users.router,       prefix="/api/users",        tags=["Users"])
app.include_router(products.router,    prefix="/api/products",     tags=["Products"])
app.include_router(orders.router,      prefix="/api/orders",       tags=["Orders"])
app.include_router(waiting_list.router,prefix="/api/waiting-list", tags=["Waiting List"])
app.include_router(reservations.router,prefix="/api/reservations", tags=["Reservations"])
app.include_router(room.router,        prefix="/api/room",         tags=["Room"])
app.include_router(categories.router,  prefix="/api/categories",   tags=["Categories"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="只允許上傳圖片檔案 (jpeg/png/webp/gif)")
    ext = os.path.splitext(file.filename or "")[1].lower() or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    dest = os.path.join(UPLOAD_DIR, filename)
    with open(dest, "wb") as f:
        f.write(await file.read())
    return {"url": f"/uploads/{filename}"}

@app.get("/")
def root():
    return {"message": "HomeFinds API is running"}
