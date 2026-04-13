import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.db import SessionLocal, engine
from app import models
from app import security

def create_admin_user():
    db = SessionLocal()
    
    # Check if admin user already exists
    existing_admin = db.query(models.User).filter(models.User.email == "admin@example.com").first()
    if existing_admin:
        print("Admin user already exists")
        db.close()
        return
    
    # Create admin user
    hashed_password = security.get_password_hash("admin123")
    admin_user = models.User(
        name="Admin User",
        email="admin@example.com",
        hashed_password=hashed_password,
        role="admin"
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print(f"Admin user created: {admin_user.name} (ID: {admin_user.id})")
    
    # Create a test event
    from datetime import date, timedelta
    test_event = models.Event(
        title="H test Quan h",
        description="S\u1ef1 ki\u1ec7n ki\u1ec3m tra \u0111\u0103ng k\u00fd tham gia",
        start_date=date.today() + timedelta(days=7),
        end_date=date.today() + timedelta(days=8),
        max_participants=50,
        status="upcoming"
    )
    
    db.add(test_event)
    db.commit()
    db.refresh(test_event)
    
    print(f"Test event created: {test_event.title} (ID: {test_event.id})")
    
    db.close()

if __name__ == "__main__":
    create_admin_user()
