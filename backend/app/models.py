from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Float, ForeignKey, Enum, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT, YEAR
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    admin = "admin"
    user = "user"
    moderator = "moderator"

class ArtistGeneration(str, PyEnum):
    truyen_thong = "truyen-thong"
    the_he_moi = "the-he-moi"

class ArticleCategory(str, PyEnum):
    lich_su = "lich-su"
    tin_tuc = "tin-tuc"
    le_hoi = "le-hoi"
    nghe_thuat = "nghe-thuat"

class MelodyCategory(str, PyEnum):
    co = "co"
    moi = "moi"
    cai_bien = "cai-bien"

class Difficulty(str, PyEnum):
    de = "de"
    trung_binh = "trung-binh"
    kho = "kho"

class LocationType(str, PyEnum):
    lang_quan_ho = "lang-quan-ho"
    le_hoi = "le-hoi"
    dien_xuong = "dien-xuong"

class MediaType(str, PyEnum):
    image = "image"
    video = "video"
    audio = "audio"

class EventStatus(str, PyEnum):
    upcoming = "upcoming"
    ongoing = "ongoing"
    finished = "finished"

class ArticleStatus(str, PyEnum):
    draft = "draft"
    published = "published"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, index=True)
    content = Column(Text) # Changed from LONGTEXT for SQLite compatibility
    excerpt = Column(Text)
    image_url = Column(String(500))
    category = Column(Enum(ArticleCategory), default=ArticleCategory.tin_tuc)
    views = Column(Integer, default=0)
    status = Column(Enum(ArticleStatus), default=ArticleStatus.draft)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    author = relationship("User")

class Melody(Base):
    __tablename__ = "melodies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True)
    description = Column(Text)
    lyrics = Column(Text)
    audio_url = Column(String(500))
    video_url = Column(String(500))
    category = Column(Enum(MelodyCategory), default=MelodyCategory.co, index=True)
    village = Column(String(255), index=True)
    difficulty = Column(Enum(Difficulty), default=Difficulty.trung_binh)
    image_url = Column(String(500))
    duration = Column(String(50))
    artist_id = Column(Integer, ForeignKey("artists.id"))
    views = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    artist = relationship("Artist")

class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True)
    birth_year = Column(Integer) # Changed from YEAR
    death_year = Column(Integer, nullable=True) # Changed from YEAR
    description = Column(Text)
    biography = Column(Text)
    contributions = Column(Text)
    performances = Column(Integer, default=0)
    image_url = Column(String(500))
    village = Column(String(255))
    achievements = Column(Text)
    generation = Column(Enum(ArtistGeneration), default=ArtistGeneration.truyen_thong)
    created_at = Column(DateTime, server_default=func.now())

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True)
    address = Column(Text)
    latitude = Column(Float(10, 8))
    longitude = Column(Float(11, 8))
    description = Column(Text)
    festival = Column(String(255))
    image_url = Column(String(500))
    type = Column(Enum(LocationType), default=LocationType.lang_quan_ho, index=True)
    created_at = Column(DateTime, server_default=func.now())

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, index=True)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"))
    image_url = Column(String(500))
    status = Column(Enum(EventStatus), default=EventStatus.upcoming)
    max_participants = Column(Integer, default=100)
    created_at = Column(DateTime, server_default=func.now())
    location = relationship("Location")

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))
    type = Column(Enum(MediaType), nullable=False)
    alt_description = Column(String(500))
    melody_id = Column(Integer, ForeignKey("melodies.id", ondelete="CASCADE"))
    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="CASCADE"))
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"))
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    upload_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    melody_id = Column(Integer, ForeignKey("melodies.id", ondelete="CASCADE"))
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.now())
    user = relationship("User")
