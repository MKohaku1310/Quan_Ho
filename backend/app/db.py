from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory for the backend
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL is not provided, use default relative to backend directory
if not SQLALCHEMY_DATABASE_URL:
    db_path = BASE_DIR / "quan_ho.db"
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
    print(f"INFO: DATABASE_URL not found in .env, using default: {SQLALCHEMY_DATABASE_URL}")

# Ensure the database URL for SQLite works correctly on Windows (needs 3 slashes)
if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///./"):
    # Convert relative path to absolute to avoid confusion
    rel_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///./", "")
    abs_path = (BASE_DIR / rel_path).resolve()
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{abs_path}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

