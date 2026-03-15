try:
    from app import models, schemas, crud
    from app.db import engine, SessionLocal
    from app.router import auth, melodies, artists, articles, locations, events
    print("All imports successful!")
except ImportError as e:
    print(f"Import Error: {e}")
except Exception as e:
    print(f"Other Error: {e}")
