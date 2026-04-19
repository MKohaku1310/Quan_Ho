from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator
from typing import Optional, List, Any, Union
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
    created_at: Optional[datetime] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[UserRole] = None

class UserSelfUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserAdminUpdate(UserSelfUpdate):
    role: Optional[UserRole] = None

class UserRoleUpdate(BaseModel):
    role: UserRole

class PasswordChange(BaseModel):
    old_password: str
    new_password: str




class MelodyBase(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    lyrics: Optional[str] = None
    lyrics_en: Optional[str] = None
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
    name_en: Optional[str] = None
    slug: Optional[str] = None
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    biography: Optional[str] = None
    biography_en: Optional[str] = None
    contributions: Optional[str] = None
    contributions_en: Optional[str] = None
    performances: int = 0
    image_url: Optional[str] = None
    village: Optional[str] = None
    achievements: Optional[str] = None
    achievements_en: Optional[str] = None
    generation: ArtistGeneration = ArtistGeneration.truyen_thong

class ArtistCreate(ArtistBase):
    pass

class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    generation: Optional[ArtistGeneration] = None

class Artist(ArtistBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class ArticleCreate(BaseModel):
    title: str
    title_en: Optional[str] = None
    slug: Optional[str] = None
    content: str
    content_en: Optional[str] = None
    excerpt: Optional[str] = None
    excerpt_en: Optional[str] = None
    image_url: Optional[str] = None
    category: ArticleCategory = ArticleCategory.tin_tuc
    status: ArticleStatus = ArticleStatus.draft

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    title_en: Optional[str] = None
    content: Optional[str] = None
    content_en: Optional[str] = None
    excerpt: Optional[str] = None
    excerpt_en: Optional[str] = None
    image_url: Optional[str] = None
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
    description_en: Optional[str] = None
    history: Optional[str] = None
    history_en: Optional[str] = None
    culture: Optional[str] = None
    culture_en: Optional[str] = None
    festival: Optional[str] = None
    festival_en: Optional[str] = None
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
    title_en: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    image_url: Optional[str] = None
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
    registered_count: Optional[int] = 0
    available_slots: Optional[int] = None
    is_registered: Optional[bool] = False
    location: Optional[str] = None
    created_at: datetime

    @field_validator("location", mode="before")
    @classmethod
    def validate_location(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        if isinstance(v, str):
            return v
        if hasattr(v, "name"):
            return v.name
        if isinstance(v, dict) and "name" in v:
            return v["name"]
        return str(v)

class CommentBase(BaseModel):
    content: str
    melody_id: Optional[int] = None
    article_id: Optional[int] = None
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    @model_validator(mode='after')
    def validate_target(self):
        has_melody = self.melody_id is not None
        has_article = self.article_id is not None
        if has_melody == has_article:
            raise ValueError("Exactly one of melody_id or article_id is required")
        return self

class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    user: Optional[User] = None
    created_at: datetime

class EventRegistrationCreate(BaseModel):
    name: str
    email: str
    phone: str
    note: Optional[str] = None

class EventRegistration(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    event_id: int
    user_id: int
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime
    status: str
    user: Optional[User] = None
    event: Optional[Event] = None

class UserActivity(BaseModel):
    id: int
    type: str  # 'registration', 'comment'
    title: str
    date: datetime
    details: Optional[str] = None

class FavoriteCreate(BaseModel):
    melody_id: int

class FavoriteItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    melody_id: int
    created_at: Optional[datetime] = None
    melody: Optional[Melody] = None
