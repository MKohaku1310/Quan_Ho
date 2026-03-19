try:
    import fastapi
    import sqlalchemy
    from sqlalchemy.orm import Session
    from app import models, schemas, crud
    from app.db import engine, SessionLocal
    from app.router import auth, melodies, artists, articles, locations, events
    print("ALL_IMPORTS_OK_VERIFIED")
except ImportError as e:
    print(f"IMPORT_ERROR: {e}")
except Exception as e:
    print(f"OTHER_ERROR: {e}")
