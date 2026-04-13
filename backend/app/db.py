from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# Thư mục gốc cho backend
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Nếu DATABASE_URL không được cung cấp, sử dụng mặc định tương đối với thư mục backend
if not SQLALCHEMY_DATABASE_URL:
    db_path = BASE_DIR / "quan_ho.db"
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
    print(f"INFO: DATABASE_URL not found in .env, using default: {SQLALCHEMY_DATABASE_URL}")

# Đảm bảo URL database SQLite hoạt động đúng trên Windows (cần 3 dấu gạch chéo)
if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///./"):
    # Chuyển đường dẫn tương đối thành tuyệt đối để tránh nhầm lẫn
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

