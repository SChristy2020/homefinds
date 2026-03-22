import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, products, orders, waiting_list, reservations, room, categories, marketing

from pathlib import Path
load_dotenv(Path(__file__).parent.parent / ".env")
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)

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

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="只允許上傳圖片檔案 (jpeg/png/webp/gif)")
    data = await file.read()
    result = cloudinary.uploader.upload(data, folder="homefinds")
    return {"url": result["secure_url"]}

@app.get("/")
def root():
    return {"message": "HomeFinds API is running"}
