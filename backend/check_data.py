from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models

db = SessionLocal()
locations = db.query(models.Location).all()
print(f"Total locations: {len(locations)}")
for loc in locations:
    print(f" - {loc.name} (Address: {loc.address})")
db.close()
