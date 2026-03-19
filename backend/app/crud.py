from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from app import models, schemas, security
import hashlib
# CRUD Người dùng
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

# CRUD Làn điệu
def create_melody(db: Session, melody: schemas.MelodyCreate) -> models.Melody:
    db_melody = models.Melody(**melody.model_dump())
    db.add(db_melody)
    db.commit()
    db.refresh(db_melody)
    return db_melody

def get_melody(db: Session, melody_id: int) -> Optional[models.Melody]:
    return db.query(models.Melody).filter(models.Melody.id == melody_id).first()

def get_melodies(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    village: Optional[str] = None,
    category: Optional[str] = None
) -> List[models.Melody]:
    query = db.query(models.Melody)
    if village:
        query = query.filter(models.Melody.village == village)
    if category:
        query = query.filter(models.Melody.category == category)
    return query.offset(skip).limit(limit).all()

def get_melodies_by_search(db: Session, search: str, limit: int = 20) -> List[models.Melody]:
    return db.query(models.Melody).filter(
        models.Melody.name.contains(search) | 
        models.Melody.description.contains(search) |
        models.Melody.lyrics.contains(search)
    ).limit(limit).all()

# CRUD Nghệ nhân
def create_artist(db: Session, artist: schemas.ArtistCreate) -> models.Artist:
    db_artist = models.Artist(**artist.model_dump())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def get_artist(db: Session, artist_id: int) -> Optional[models.Artist]:
    return db.query(models.Artist).filter(models.Artist.id == artist_id).first()

def get_artists(db: Session, skip: int = 0, limit: int = 100) -> List[models.Artist]:
    return db.query(models.Artist).offset(skip).limit(limit).all()

# CRUD Bài viết
def create_article(db: Session, article: schemas.ArticleCreate, author_id: Optional[int]) -> models.Article:
    db_article = models.Article(**article.model_dump(), author_id=author_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_articles(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[models.Article]:
    query = db.query(models.Article)
    if category:
        query = query.filter(models.Article.category == category)
    return query.offset(skip).limit(limit).all()

def get_article(db: Session, article_id: int) -> Optional[models.Article]:
    return db.query(models.Article).filter(models.Article.id == article_id).first()

# CRUD Địa điểm
def create_location(db: Session, location: schemas.LocationCreate) -> models.Location:
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_locations(db: Session, skip: int = 0, limit: int = 100, type: Optional[str] = None) -> List[models.Location]:
    query = db.query(models.Location)
    if type:
        query = query.filter(models.Location.type == type)
    return query.offset(skip).limit(limit).all()

# CRUD Sự kiện
def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session, skip: int = 0, limit: int = 100) -> List[models.Event]:
    return db.query(models.Event).offset(skip).limit(limit).all()
