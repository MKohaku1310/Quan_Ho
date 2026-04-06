from app.db import SessionLocal
from app import models

def check_counts():
    db = SessionLocal()
    try:
        print(f"Users: {db.query(models.User).count()}")
        print(f"Artists: {db.query(models.Artist).count()}")
        print(f"Locations: {db.query(models.Location).count()}")
        print(f"Melodies: {db.query(models.Melody).count()}")
        print(f"Articles: {db.query(models.Article).count()}")
        print(f"Events: {db.query(models.Event).count()}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_counts()
