from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from app import models, schemas, security
import hashlib
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

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, user_id: int, new_password: str):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db_user.hashed_password = security.get_password_hash(new_password)
    db.commit()
    return True

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

def update_user_role(db: Session, user_id: int, role: str) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db_user.role = role
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_activities(db: Session, user_id: int) -> List[dict]:
    activities = []
    
    # Favorites
    favs = db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()
    for f in favs:
        activities.append({
            "id": f.id,
            "type": 'favorite',
            "title": f"Yêu thích: {f.melody.name}" if f.melody else "Yêu thích giai điệu",
            "date": f.created_at,
            "details": f.melody.description[:50] + "..." if f.melody and f.melody.description and len(f.melody.description) > 50 else (f.melody.description if f.melody else "")
        })
    
    # History
    hist = db.query(models.History).filter(models.History.user_id == user_id).order_by(models.History.created_at.desc()).limit(20).all()
    for h in hist:
        activities.append({
            "id": h.id,
            "type": 'history',
            "title": f"Đã nghe: {h.melody.name}" if h.melody else "Nghe giai điệu",
            "date": h.created_at,
            "details": f"Thời gian: {h.created_at.strftime('%H:%M %d/%m/%Y')}"
        })
    
    # Events
    regs = db.query(models.EventRegistration).filter(models.EventRegistration.user_id == user_id).all()
    for r in regs:
        activities.append({
            "id": r.id,
            "type": "registration",
            "title": f"Đăng ký: {r.event.title}" if r.event else "Đăng ký sự kiện",
            "date": r.created_at,
            "details": f"Trạng thái: {r.status}"
        })
        
    # Comments
    comments = db.query(models.Comment).filter(models.Comment.user_id == user_id).all()
    for c in comments:
        activities.append({
            "id": c.id,
            "type": "comment",
            "title": "Bình luận",
            "date": c.created_at,
            "details": c.content[:50] + "..." if len(c.content) > 50 else c.content
        })
        
    # Sort by date
    activities.sort(key=lambda x: x['date'], reverse=True)
    return activities


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

def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session, skip: int = 0, limit: int = 100) -> List[models.Event]:
    return db.query(models.Event).offset(skip).limit(limit).all()

def create_event_registration(db: Session, event_id: int, user_id: int, registration_data: dict) -> models.EventRegistration:
    db_reg = models.EventRegistration(
        event_id=event_id,
        user_id=user_id,
        status="registered"
    )
    db.add(db_reg)
    db.commit()
    db.refresh(db_reg)
    
    # Mock Email Notification
    print(f"MOCK EMAIL: Gửi thông báo đăng ký thành công cho người dùng ID {user_id} tại sự kiện {event_id}")
    
    return db_reg

def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int) -> models.Comment:
    db_comment = models.Comment(**comment.model_dump(), user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments(
    db: Session, 
    melody_id: Optional[int] = None, 
    article_id: Optional[int] = None,
    skip: int = 0, 
    limit: int = 50
) -> List[models.Comment]:
    query = db.query(models.Comment)
    if melody_id:
        query = query.filter(models.Comment.melody_id == melody_id)
    if article_id:
        query = query.filter(models.Comment.article_id == article_id)
    return query.order_by(models.Comment.created_at.desc()).offset(skip).limit(limit).all()

def update_melody(db: Session, melody_id: int, melody_update: dict) -> Optional[models.Melody]:
    db_melody = get_melody(db, melody_id)
    if not db_melody:
        return None
    for key, value in melody_update.items():
        if hasattr(db_melody, key):
            setattr(db_melody, key, value)
    db.commit()
    db.refresh(db_melody)
    return db_melody

def delete_melody(db: Session, melody_id: int) -> bool:
    db_melody = get_melody(db, melody_id)
    if not db_melody: return False
    db.delete(db_melody)
    db.commit()
    return True

def update_artist(db: Session, artist_id: int, artist_update: dict) -> Optional[models.Artist]:
    db_artist = get_artist(db, artist_id)
    if not db_artist:
        return None
    for key, value in artist_update.items():
        if hasattr(db_artist, key):
            setattr(db_artist, key, value)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def delete_artist(db: Session, artist_id: int) -> bool:
    db_artist = get_artist(db, artist_id)
    if not db_artist: return False
    db.delete(db_artist)
    db.commit()
    return True

def delete_article(db: Session, article_id: int) -> bool:
    db_article = get_article(db, article_id)
    if not db_article: return False
    db.delete(db_article)
    db.commit()
    return True

def update_article(db: Session, article_id: int, article_update: dict) -> Optional[models.Article]:
    db_article = get_article(db, article_id)
    if not db_article: return None
    for key, value in article_update.items():
        if hasattr(db_article, key):
            setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

def delete_location(db: Session, location_id: int) -> bool:
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not db_location: return False
    db.delete(db_location)
    db.commit()
    return True

def update_location(db: Session, location_id: int, location_update: dict) -> Optional[models.Location]:
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not db_location: return None
    for key, value in location_update.items():
        if hasattr(db_location, key):
            setattr(db_location, key, value)
    db.commit()
    db.refresh(db_location)
    return db_location

