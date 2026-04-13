from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, models
from app.db import get_db

from app.router import auth
from app.router.auth import get_current_active_admin

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=schemas.Event)
def create_event(
    event: schemas.EventCreate, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    return crud.create_event(db=db, event=event)

@router.put("/{event_id}", response_model=schemas.Event)
def update_event(
    event_id: int, 
    event_update: dict, 
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

@router.get("/", response_model=List[schemas.Event])
def read_events(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return crud.get_events(db, skip=skip, limit=limit)

@router.get("/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.post("/{event_id}/register", response_model=schemas.EventRegistration)
async def register_for_event(
    event_id: int, 
    reg_data: dict, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(auth.get_current_user)
):
    # Kiểm tra xem đã đăng ký chưa
    existing = db.query(models.EventRegistration).filter(
        models.EventRegistration.event_id == event_id,
        models.EventRegistration.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already registered for this event")
        
    return crud.create_event_registration(db, event_id, current_user.id, reg_data)
