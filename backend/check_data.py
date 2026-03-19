import sys
import io
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models

# Force UTF-8 for Vietnamese characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

db = SessionLocal()


def check_model(model_class, label):
    items = db.query(model_class).all()
    print(f"Total {label}: {len(items)}")
    for item in items[:3]:  # Print first 3 items
        name = getattr(item, 'name', getattr(item, 'title', 'No Name/Title'))
        print(f" - {name}")
    if len(items) > 3:
        print(f" ... and {len(items) - 3} more")

print("--- Database Status ---")
check_model(models.Location, "locations")
check_model(models.Artist, "artists")
check_model(models.Article, "articles/news")
check_model(models.Melody, "melodies")
check_model(models.Event, "events")
check_model(models.User, "users")

db.close()

