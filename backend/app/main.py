from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.db import engine, Base
from app.router import auth, melodies, artists, articles, locations, events, comments, chatbot
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quan Họ Bắc Ninh API", version="1.0.0")

# Thiết lập CORS
cors_origins_raw = os.getenv("CORS_ORIGINS", "")
if cors_origins_raw:
    allow_origins = [o.strip() for o in cors_origins_raw.split(",")]
else:
    # Mặc định an toàn bao gồm localhost và truy cập LAN tiềm năng
    allow_origins = [
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:8080", "http://127.0.0.1:8080",
        "*" # Rộng gàng cho debug local, nên giới hạn trong production
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api")
app.include_router(melodies.router, prefix="/api")
app.include_router(artists.router, prefix="/api")
app.include_router(articles.router, prefix="/api")
app.include_router(locations.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(chatbot.router, prefix="/api")

# File tĩnh được xử lý bởi frontend theo yêu cầu người dùng


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Quan Họ Bắc Ninh API - Ready!"}

