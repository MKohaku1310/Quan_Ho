import sys
import os
from pathlib import Path

# Add backend to sys.path
backend_path = Path(__file__).resolve().parent
sys.path.append(str(backend_path))

from app.db import SessionLocal
from app import models, security

def create_admin():
    db = SessionLocal()
    try:
        admin_email = "admin@example.com"
        db_user = db.query(models.User).filter(models.User.email == admin_email).first()
        if db_user:
            print(f"Admin already exists: {admin_email}")
            # Ensure it has admin role
            if db_user.role != models.UserRole.admin:
                db_user.role = models.UserRole.admin
                db.commit()
                print("Updated role to admin")
            return

        hashed_password = security.get_password_hash("admin123")
        new_admin = models.User(
            name="Administrator",
            email=admin_email,
            hashed_password=hashed_password,
            role=models.UserRole.admin
        )
        db.add(new_admin)
        db.commit()
        print(f"Admin created successfully: {admin_email} / admin123")
    except Exception as e:
        print(f"Error creating admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
