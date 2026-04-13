import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.db import SessionLocal
from app import models, security

db = SessionLocal()
admin = db.query(models.User).filter(models.User.email == 'admin@example.com').first()
if admin:
    print(f'Admin found: {admin.name}, Role: {admin.role}')
    print(f'Password verification: {security.verify_password("admin123", admin.hashed_password)}')
else:
    print('Admin not found')
db.close()
