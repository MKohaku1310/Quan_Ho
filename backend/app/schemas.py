from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"

class ArtistGeneration(str, Enum):
    truyen_thong = "truyen-thong"
    the_he_moi = "the-he-moi"

class ArticleCategory(str, Enum):
    lich_su = "lich-su"
    tin_tuc = "tin-tuc"
    le_hoi = "le-hoi"
    nghe_thuat = "nghe-thuat"

class MelodyCategory(str, Enum):
    co = "co"
    moi = "moi"
    cai_bien = "cai-bien"

class Difficulty(str, Enum):
    de = "de"
    trung_binh = "trung-binh"
    kho = "kho"

class LocationType(str, Enum):
    lang_quan_ho = "lang-quan-ho"
    le_hoi = "le-hoi"
    dien_xuong = "dien-xuong"

class MediaType(str, Enum):
    image = "image"
    video = "video"
    audio = "audio"

class EventStatus(str, Enum):
    upcoming = "upcoming"
    ongoing = "ongoing"
    finished = "finished"

class ArticleStatus(str, Enum):
    draft = "draft"
    published = "published"

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role: UserRole
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[UserRole] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str




class MelodyBase(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    lyrics: Optional[str] = None
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    duration: Optional[str] = None
    artist_id: Optional[int] = None
    category: MelodyCategory = MelodyCategory.co
    village: Optional[str] = None
    difficulty: Difficulty = Difficulty.trung_binh

class MelodyCreate(MelodyBase):
    pass

class MelodyUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[MelodyCategory] = None
    village: Optional[str] = None
    difficulty: Optional[Difficulty] = None

class Melody(MelodyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    views: int = 0
    created_at: datetime

class ArtistBase(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    biography: Optional[str] = None
    contributions: Optional[str] = None
    performances: int = 0
    image_url: Optional[str] = None
    village: Optional[str] = None
    achievements: Optional[str] = None
    generation: ArtistGeneration = ArtistGeneration.truyen_thong

class ArtistCreate(ArtistBase):
    pass

class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    generation: Optional[ArtistGeneration] = None

class Artist(ArtistBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    created_at: datetime

class ArticleCreate(BaseModel):
    title: str
    slug: Optional[str] = None
    content: str
    excerpt: Optional[str] = None
    category: ArticleCategory = ArticleCategory.tin_tuc
    status: ArticleStatus = ArticleStatus.draft

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[ArticleCategory] = None
    status: Optional[ArticleStatus] = None

class Article(ArticleCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    views: int = 0
    author_id: Optional[int] = None
    created_at: datetime

class LocationBase(BaseModel):
    name: str
    slug: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    district: Optional[str] = None
    artist_count: Optional[int] = 0
    featured_songs: Optional[str] = None
    badges: Optional[str] = None
    description: Optional[str] = None
    history: Optional[str] = None
    culture: Optional[str] = None
    festival: Optional[str] = None
    type: LocationType = LocationType.lang_quan_ho
    image_url: Optional[str] = None

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    district: Optional[str] = None
    artist_count: Optional[int] = None
    featured_songs: Optional[str] = None
    badges: Optional[str] = None
    type: Optional[LocationType] = None

class Location(LocationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class EventBase(BaseModel):
    title: str
    slug: Optional[str] = None
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    location_id: Optional[int] = None
    status: EventStatus = EventStatus.upcoming
    max_participants: int = 100

class EventCreate(EventBase):
    pass

class Event(EventBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_url: Optional[str] = None
    created_at: datetime

class CommentBase(BaseModel):
    content: str
    melody_id: Optional[int] = None
    article_id: Optional[int] = None
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    user: User
    created_at: datetime

class EventRegistration(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    event_id: int
    user_id: int
    created_at: datetime
    status: str
    event: Optional[Event] = None

class UserActivity(BaseModel):
    id: int
    type: str  # 'registration', 'comment'
    title: str
    date: datetime
    details: Optional[str] = None
