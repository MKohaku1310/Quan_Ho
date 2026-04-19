from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app import crud, schemas, models, security
from app.db import get_db

from app.router import auth
from app.router.auth import get_current_active_admin

router = APIRouter(prefix="/events", tags=["events"])
oauth2_optional = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def _build_event_response(db_event: models.Event, db: Session, user_id: Optional[int] = None) -> schemas.Event:
    registered_count = crud.get_event_registration_count(db, db_event.id)
    available_slots = max((db_event.max_participants or 0) - registered_count, 0)
    is_registered = False
    if user_id:
        is_registered = db.query(models.EventRegistration).filter(
            models.EventRegistration.event_id == db_event.id,
            models.EventRegistration.user_id == user_id
        ).first() is not None

    location_name = db_event.location.name if db_event.location else None
    return schemas.Event.model_validate({
        **db_event.__dict__,
        "registered_count": registered_count,
        "available_slots": available_slots,
        "is_registered": is_registered,
        "location": location_name
    })

def _get_optional_user_id(token: Optional[str], db: Session) -> Optional[int]:
    if not token:
        return None
    try:
        payload = security.decode_access_token(token)
        email = payload.get("sub")
        if not email:
            return None
        user = crud.get_user_by_email(db, email)
        return user.id if user else None
    except Exception:
        return None

@router.post("", response_model=schemas.Event)
def create_event(
    event: schemas.EventCreate, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    return crud.create_event(db=db, event=event)

@router.put("/{event_id}", response_model=schemas.Event)
def update_event(
    event_id: int, 
    event_update: Dict[str, Any] = Body(...), 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    # Cập nhật sự kiện trực tiếp từ database
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in event_update.items():
        if hasattr(db_event, key):
            setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}")
def delete_event(
    event_id: int, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"}

@router.get("", response_model=List[schemas.Event])
def read_events(
    skip: int = 0, 
    limit: int = 100, 
    token: Optional[str] = Depends(oauth2_optional),
    db: Session = Depends(get_db)
):
    user_id = _get_optional_user_id(token, db)
    events = crud.get_events(db, skip=skip, limit=limit)
    return [_build_event_response(event, db, user_id=user_id) for event in events]

@router.get("/count")
def get_events_count(db: Session = Depends(get_db)):
    return {"total": crud.count_events(db)}

@router.get("/{event_id}", response_model=schemas.Event)
def read_event(
    event_id: int,
    token: Optional[str] = Depends(oauth2_optional),
    db: Session = Depends(get_db)
):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    user_id = _get_optional_user_id(token, db)
    return _build_event_response(db_event, db, user_id=user_id)

@router.get("/registrations/all", response_model=List[schemas.EventRegistration])
def read_all_registrations(
    skip: int = 0,
    limit: int = 100,
    admin: schemas.User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    """Lấy danh sách tất cả các lượt đăng ký sự kiện (chỉ dành cho Admin)"""
    return db.query(models.EventRegistration).order_by(models.EventRegistration.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/registrations/count")
def get_registrations_count(
    event_id: Optional[int] = None,
    admin: schemas.User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    return {"total": crud.count_registrations(db, event_id=event_id)}

@router.post("/{event_id}/register", response_model=schemas.EventRegistration)
async def register_for_event(
    event_id: int, 
    reg_data: schemas.EventRegistrationCreate,
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(auth.get_current_user)
):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    registered_count = crud.get_event_registration_count(db, event_id)
    if registered_count >= (db_event.max_participants or 0):
        raise HTTPException(status_code=409, detail="Event is full")

    # Kiểm tra xem đã đăng ký chưa
    existing = db.query(models.EventRegistration).filter(
        models.EventRegistration.event_id == event_id,
        models.EventRegistration.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already registered for this event")
        
    return crud.create_event_registration(db, event_id, current_user.id, reg_data.model_dump())

@router.get("/{event_id}/registrations", response_model=List[schemas.EventRegistration])
def read_event_registrations(
    event_id: int,
    admin: schemas.User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.get_event_registrations(db, event_id)
