from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.db import engine, Base
from app.router import auth, melodies, artists, articles, locations, events, comments, chatbot, favorites
import os
from sqlalchemy import text

Base.metadata.create_all(bind=engine)

def _ensure_event_registration_columns():
    with engine.begin() as conn:
        try:
            rows = conn.execute(text("PRAGMA table_info(event_registrations)")).fetchall()
        except Exception:
            return
        existing = {row[1] for row in rows}
        for column_name, column_type in [
            ("name", "VARCHAR(255)"),
            ("email", "VARCHAR(255)"),
            ("phone", "VARCHAR(20)"),
            ("note", "TEXT"),
        ]:
            if column_name not in existing:
                conn.execute(text(f"ALTER TABLE event_registrations ADD COLUMN {column_name} {column_type}"))

_ensure_event_registration_columns()

app = FastAPI(title="Quan Họ Bắc Ninh API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080", "http://127.0.0.1:8080",
        "http://localhost:8000", "http://127.0.0.1:8000"
    ],
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
app.include_router(favorites.router, prefix="/api")

# File tĩnh được xử lý bởi frontend theo yêu cầu người dùng


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Quan Họ Bắc Ninh API - Ready!"}

