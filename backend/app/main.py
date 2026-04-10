from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.db import engine, Base
from app.router import auth, melodies, artists, articles, locations, events
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quan Họ Bắc Ninh API", version="1.0.0")

frontend_origin = os.getenv("CORS_ORIGIN")
if frontend_origin:
    allow_origins = [frontend_origin]
else:
    allow_origins = [
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
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

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")

if os.path.exists(frontend_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail=f"API route '{full_path}' not found")
        
        file_path = os.path.join(frontend_path, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        
        return FileResponse(os.path.join(frontend_path, "index.html"))
else:
    @app.get("/")
    def read_root():
        return {"message": "Quan Họ Bắc Ninh API - Ready! (Frontend build not found)"}
